"""Streamlit visualizer.

streamlit run scripts/visualizer/visualizer.py -- --data_dir data/outputs
"""
import re
import json
import random
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
from glob import glob
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st

# default wide mode
st.set_page_config(layout="wide", page_title="Interaction-Eval Output Visualizer")

st.title("Interaction-Eval Output Visualizer")

# Select your data directory
query_params = st.experimental_get_query_params()
glob_pattern = st.text_input(
    "Enter the glob to your data directory.\nFor example: `/path/to/your/mint/data/outputs/CodeLlama*/F=None/max5_p2+tool+cd/**/*results.jsonl`",
    key="data_dir",
    value=query_params.get(
        "data_dir",
        ["/path/to/your/mint/data/outputs/**/*results.jsonl"],
    )[0],
)
st.experimental_set_query_params(glob_pattern=glob_pattern)

filepaths = list(set(glob(glob_pattern, recursive=True)))
st.write(f"Matching glob pattern: `{glob_pattern}`. **{len(filepaths)}** files found.")


def parse_filepath(filepath):
    # gpt-3.5-turbo-0613/F=gpt-3.5-turbo-16k-0613/PHF=no_GT-textual/max5_p2+tool+cd/code_generation/humaneval/results.jsonl
    # gpt-3.5-turbo-0613/F=None/max5_p2+tool+cd/code_generation/humaneval/results.jsonl
    splited = (
        filepath[filepath.find("data/outputs/") + len("data/outputs/") :]
        .lstrip("/")
        .split("/")
    )
    try:
        agent_model_name = splited[0]
        feedback_model_name = splited[1].split("=")[1]
        if feedback_model_name != "None":
            feedback_setting = splited[2]
        else:
            feedback_setting = "None"
        task_name = splited[-2]
        task_type = splited[-3]
        exp_setting = splited[-4]
        return {
            "agent_model_name": agent_model_name,
            "feedback_model_name": feedback_model_name,
            "feedback_setting": feedback_setting,
            "task_name": task_name,
            "task_type": task_type,
            "exp_setting": exp_setting,
            "filepath": filepath,
        }
    except Exception as e:
        st.write([filepath, e, splited])


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


def dataframe_with_selections(
    df,
    selected_values=None,
    selected_col="filepath",
):
    # https://docs.streamlit.io/knowledge-base/using-streamlit/how-to-get-row-selections
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Set the initial state of "Select" column based on query parameters
    if selected_values:
        df_with_selections.loc[
            df_with_selections[selected_col].isin(selected_values), "Select"
        ] = True

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop("Select", axis=1)


filepaths = pd.DataFrame(list(map(parse_filepath, filepaths)))

# ===== Select a file to visualize =====

filepaths = filepaths.sort_values(
    [
        "agent_model_name",
        "feedback_model_name",
        "task_type",
        "task_name",
        "feedback_setting",
        "exp_setting",
    ]
)

st.markdown("**Select file(s) to visualize**")
filepaths = filter_dataframe(filepaths)
# Make these two buttons are on the same row
# col1, col2 = st.columns(2)
col1, col2 = st.columns([0.08, 1])
select_all = col1.button("Select all")
deselect_all = col2.button("Deselect all")
selected_values = query_params.get("filepaths", None)
selected_values = filepaths["filepath"].tolist() if select_all else selected_values
selected_values = [] if deselect_all else selected_values

selection = dataframe_with_selections(
    filepaths,
    selected_values=selected_values,
    selected_col="filepath",
)
# st.write("Your selection:")
# st.write(selection)
select_filepaths = selection["filepath"].tolist()
# update query params
st.experimental_set_query_params(glob_pattern=glob_pattern, filepaths=select_filepaths)

data = []
for filepath in select_filepaths:
    with open(filepath, "r") as f:
        for l in f.readlines():
            data.append(json.loads(l))
st.write(f"{len(data)} rows found.")

# ===== Task-level dashboard =====


def agg_stats(data):
    stats = []
    for idx, entry in enumerate(data):
        # if len(entry["state"]["history"]) % 2 != 0: continue
        task = {
            k: v for k, v in entry["task"].items() if k not in ["prompt", "reference"]
        }
        if "metadata" in task:
            for k, v in task["metadata"].items():
                task[k] = v
            del task["metadata"]

        stats.append(
            {
                "idx": idx,
                "success": entry["state"]["success"],
                "n_turns": len(entry["state"]["history"]) // 2,
                "terminate_reason": entry["state"]["terminate_reason"],
                "agent_action_count": entry["state"]["agent_action_count"],
                **task,
            }
        )
    return pd.DataFrame(stats)


st.markdown("---")
stats_df = agg_stats(data)
if len(stats_df) == 0:
    st.write("No data to visualize.")
    st.stop()
success_count = stats_df["success"].sum()
st.markdown(
    f"**Success Rate: {success_count / len(data):2%}**: {success_count} / {len(data)} rows are successful."
)


def plot_stats(stats_df):
    # 1. Plot a distribution of terminate_reason, also show percentage
    # fig, ax = plt.subplots(figsize=(6, 1))
    # sns.countplot(y="terminate_reason", data=stats_df, ax=ax)
    # ax.set_title("Distribution of Terminate Reason")
    # ax.set_xlabel("Count")
    # ax.set_ylabel("")
    # # add percentage
    # total = len(stats_df)
    # for p in ax.patches:
    #     percentage = "{:.1f}%".format(100 * p.get_width() / total)
    #     x = p.get_x() + p.get_width()
    #     y = p.get_y() + p.get_height() / 2
    #     ax.annotate(percentage, (x, y))
    # st.pyplot(fig, use_container_width=False)
    terminate_reason_count = (
        stats_df["terminate_reason"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "terminate_reason", "terminate_reason": "count"})
    )
    chart = (
        alt.Chart(terminate_reason_count)
        .mark_bar()
        .encode(
            x=alt.X("count", type="quantitative", title=""),
            y=alt.Y("terminate_reason", type="nominal", title=""),
            # color=alt.Color("variable", type="nominal", title=""),
            # order=alt.Order("variable", sort="descending"),
        )
    )
    st.altair_chart(chart, use_container_width=True)

    # 1. plot success rate changes over n_turns
    fig, ax = plt.subplots(figsize=(6, 3))
    max_turns = stats_df["n_turns"].max()
    _df = []
    for turn_id in range(1, max_turns + 1):
        _df.append(
            {
                "n_turns": turn_id,
                "success_rate": stats_df[stats_df["n_turns"] <= turn_id][
                    "success"
                ].sum()
                / len(stats_df),
            }
        )
    _df = pd.DataFrame(_df)
    # sns.lineplot(x="n_turns", y="success_rate", data=_df, ax=ax)
    # ax.set_title("Task Success Rate vs. Number of Turns")
    # ax.set_xlabel("Number of Turns")
    # ax.set_ylabel("Success Rate")
    # make xlabel integer
    # ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    # st.pyplot(fig, use_container_width=False)

    chart = (
        alt.Chart(_df, title="Task Success Rate vs. Number of Turns")
        .mark_line()
        .encode(
            x=alt.X("n_turns", type="quantitative", title="Number of Turns"),
            y=alt.Y("success_rate", type="quantitative", title="Success Rate"),
        )
        .properties(width=550)
    )
    st.altair_chart(chart, use_container_width=True)


with st.expander("See figures", expanded=True):
    plot_stats(stats_df)

# ===== Select a row to visualize =====
st.markdown("---")
with st.expander("Stats Table", expanded=True):

    # Add a button to randomly select a row
    if st.button("Randomly Select a Row"):
        row_id = random.choice(stats_df["idx"].values)
        query_params["row_idx"] = [row_id]

    selected_row = dataframe_with_selections(
        stats_df,
        query_params.get("row_idx", None),
        selected_col="idx",
    )
    if len(selected_row) == 0:
        st.write("No row selected.")
        st.stop()
    elif len(selected_row) > 1:
        st.write("More than one row selected.")
        st.stop()
    row_id = selected_row["idx"].values[0]

    # update query params
    st.experimental_set_query_params(
        glob_pattern=glob_pattern, filepaths=select_filepaths, row_idx=[row_id]
    )

# row_id = st.number_input(
#     "Select a row to visualize", min_value=0, max_value=len(data) - 1, value=0
# )
# # row = df.iloc[row_id]

# ===== Visualize the row =====
st.write(f"Visualizing row `{row_id}`")
row_dict = data[row_id]

n_turns = len(row_dict["state"]["history"]) // 2
st.write(f"Number of turns: {n_turns}")


def visualize_row(row_dict):
    # 1. Visualize the task and metrics
    st.markdown("## Task")
    task_dict = row_dict["task"]
    st.markdown("**Prompt**")
    st.write(task_dict["prompt"])
    st.markdown("**Reference**")
    st.write(task_dict["reference"])
    st.json({k: v for k, v in task_dict.items() if k not in ["prompt", "reference"]})

    # 2. Visualize the state
    st.markdown("## State")
    state_dict = row_dict["state"]
    state_dict.pop("latest_output")
    history = state_dict.pop("history")
    st.json(state_dict)
    st.markdown("### History")

    raw_history = "\n".join(
        [f"=== {turn['role']} ===\n{turn['content']}" for turn in history]
    )
    expandable = st.expander("Show raw history", expanded=False)
    with expandable:
        st.code(raw_history)

    ROLES = [
        ("system", "blue"),
        ("user", "red"),
        ("assistant", "green"),
    ]
    REGEX_TO_HIGHLIGHT = [
        (r"<thought>(.*?)</thought>", "blue", "thought"),
        (r"<solution>(.*?)</solution>", "green", "solution"),
        (r"<execute>(.*?)</execute>", "orange", "execute"),
    ]
    for turn_id, turn_content in enumerate(history):
        if turn_id % 2 == 0:
            st.markdown(f"#### Turn {(turn_id // 2) + 1}")

        role = turn_content["role"]
        content = turn_content["content"]
        content = content.replace(
            "Available Tools (already imported for you):\n```\n", "```python\n\n"
        )
        content = content.replace("\n", "<br>")

        st.markdown(
            f"##### ROLE: <span style='color:{dict(ROLES)[role]}'>{role}</span>",
            unsafe_allow_html=True,
        )

        if turn_id == 0:
            # add newline before and after the code block
            # remove the <br> inside code block using re
            content = re.sub(
                r"```(.*?)```",
                lambda m: "\n" + m.group(0).replace("<br>", "\n") + "\n",
                content,
            )
        # use color to highlight span of regex by using re.sub
        for regex, color, field_name in REGEX_TO_HIGHLIGHT:
            content = re.sub(
                regex,
                # some hacky way to make sure the html-style prompt is escaped
                f"\n<span style='color:{color}'>&lt;{field_name}&gt; <b>\\1</b> &lt;/{field_name}&gt;</span>\n"
                if field_name != "execute"
                else lambda m: (
                    f"<span style='color:{color}'> &lt;{field_name}&gt; </span>\n"
                    + "```python\n{}\n```\n\n".format(m.group(1).replace("<br>", "\n"))
                    + f"<span style='color:{color}'> &lt;/{field_name}&gt; </span>\n"
                ),
                content,
            )
        st.write(content, unsafe_allow_html=True)
        # st.text(content)


visualize_row(row_dict)
