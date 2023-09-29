import os
import json
import pathlib
from copy import deepcopy
import glob
import shutil

# load variables from config_variables.py
from mint.configs.config_variables import (
    EVALUATED_MODEL_LIST,
    FEEDBACK_PROVIDER_LIST,
    FEEDBACK_TYPES,
    ENV_CONFIGS,
    TASK_INFO_MAP,
    TASK_TYPE_TO_TOOL_IMPORT,
    FEEDBACK_CONFIG,
    DATA_OUTPUTS_DIR,
    DATASET_DIR,
)


def build_path(
    task_name: str,
    agent_model_name: str,
    feedback_type: dict,
    feedback_model_name: str,
    env_config: str,
    prefix: str,
):
    dir_path = prefix
    # 1. first-level dir = agent model name
    dir_path = os.path.join(dir_path, agent_model_name)

    # 2. second-level dir = feedback model name
    dir_path = os.path.join(dir_path, "F=" + feedback_model_name)
    if feedback_model_name != "None":
        # 3. (optional) third-level dir = feedback type
        pseudo_human_feedback = feedback_type["pseudo_human_feedback"]
        feedback_form = feedback_type["feedback_form"]
        dir_path = os.path.join(
            dir_path, f"PHF={pseudo_human_feedback}-{feedback_form}"
        )

    # 4. fourth-level dir = env config
    max_propose_solution = env_config["max_propose_solution"]
    max_steps = env_config["max_steps"]
    use_tools = env_config["use_tools"]
    count_down = env_config["count_down"]
    cur_dir_name = f"max{max_steps}_p{max_propose_solution}"
    if use_tools:
        cur_dir_name += "+tool"
    if count_down:
        cur_dir_name += "+cd"
    dir_path = os.path.join(dir_path, cur_dir_name)

    # 5. fifth-level dir = task type
    dir_path = os.path.join(dir_path, TASK_INFO_MAP[task_name]["type"])

    # 6. sixth-level dir = task name
    dir_path = os.path.join(dir_path, task_name)
    return dir_path


def generate_config_json(
    task_name: str,
    agent_model_info: dict,
    feedback_type: dict,
    feedback_model_info: dict,
    env_config: str,
):
    model_name = agent_model_info["config"]["model_name"]
    if agent_model_info.get("exp_setting", "") == "human-eval-human":
        model_name += "-human-eval-human"
    elif agent_model_info.get("exp_setting", "") == "human-eval-gpt":
        model_name += "-human-eval-gpt"
    elif agent_model_info.get("exp_setting", "") == "human-eval-none":
        model_name += "-human-eval-none"

    output_filepath = build_path(
        task_name=task_name,
        agent_model_name=model_name,
        feedback_type=feedback_type,
        feedback_model_name=feedback_model_info["model_name"],
        env_config=env_config,
        prefix=DATA_OUTPUTS_DIR,
    )

    json_dict = {
        "agent": agent_model_info,
        "task": {
            "task_class": TASK_INFO_MAP[task_name]["class"],
            "task_type": TASK_INFO_MAP[task_name]["type"],
            "tool_imports": TASK_TYPE_TO_TOOL_IMPORT[TASK_INFO_MAP[task_name]["type"]],
        },
        "output_dir": output_filepath,
        "env_config": env_config,
    }
    pathlib.Path(output_filepath).mkdir(parents=True, exist_ok=True)
    with open(output_filepath + "/output.txt", "a") as f:
        pass

    if agent_model_info.get("exp_setting", "") == "human-eval-human":
        json_dict["task"][
            "filepath"
        ] = f"data/human_preference/test_human/{task_name}/" + (
            "test_prompts.json"
            if TASK_INFO_MAP[task_name]["type"]
            in ["reasoning", "code_generation", "vision_language"]
            else ""
        )
    elif agent_model_info.get("exp_setting", "") == "human-eval-gpt":
        json_dict["task"][
            "filepath"
        ] = f"data/human_preference/test_gpt/{task_name}/" + (
            "test_prompts.json"
            if TASK_INFO_MAP[task_name]["type"]
            in ["reasoning", "code_generation", "vision_language"]
            else ""
        )
    elif agent_model_info.get("exp_setting", "") == "human-eval-none":
        json_dict["task"][
            "filepath"
        ] = f"data/human_preference/test_none/{task_name}/" + (
            "test_prompts.json"
            if TASK_INFO_MAP[task_name]["type"]
            in ["reasoning", "code_generation", "vision_language"]
            else ""
        )
    else:
        json_dict["task"]["filepath"] = f"{DATASET_DIR}/{task_name}/" + (
            "test_prompts.json"
            if TASK_INFO_MAP[task_name]["type"]
            in ["reasoning", "code_generation", "vision_language"]
            else ""
        )
    json_dict["feedback_config"] = FEEDBACK_CONFIG
    json_dict["feedback_config"].update(feedback_type)
    json_dict["feedback_config"]["feedback_agent_config"].update(feedback_model_info)

    return json_dict


def build_json_for_all_tasks(
    agent_model_info: dict,
    feedback_type: dict,
    feedback_model_info: dict,
    env_config: dict,
):
    for task_name in TASK_INFO_MAP.keys():
        model_name = agent_model_info["config"]["model_name"]
        if agent_model_info.get("exp_setting", "") == "human-eval-human":
            model_name += "-human-eval-human"
        elif agent_model_info.get("exp_setting", "") == "human-eval-gpt":
            model_name += "-human-eval-gpt"
        elif agent_model_info.get("exp_setting", "") == "human-eval-none":
            model_name += "-human-eval-none"
        output_filepath = (
            build_path(
                task_name=task_name,
                agent_model_name=model_name,
                feedback_type=feedback_type,
                feedback_model_name=feedback_model_info["model_name"],
                env_config=env_config,
                prefix="configs/",
            )
            + ".json"
        )
        json_dict = generate_config_json(
            task_name=task_name,
            agent_model_info=agent_model_info,
            feedback_type=feedback_type,
            feedback_model_info=feedback_model_info,
            env_config=env_config,
        )

        pathlib.Path(output_filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(output_filepath, "w") as f:
            f.write(json.dumps(json_dict, indent=4) + "\n")


if __name__ == "__main__":
    # delete all existing configs
    for file in glob.glob("configs/*"):
        shutil.rmtree(file)

    # With feedback
    for agent_model_info in EVALUATED_MODEL_LIST:
        for feedback_model_info in FEEDBACK_PROVIDER_LIST:
            for env_config in ENV_CONFIGS:

                # If no feedback is provided
                if feedback_model_info["agent_class"] == "None":
                    build_json_for_all_tasks(
                        agent_model_info=agent_model_info,
                        feedback_type={
                            "pseudo_human_feedback": "None",
                            "feedback_form": "None",
                        },
                        feedback_model_info=feedback_model_info,
                        env_config=env_config,
                    )

                # If feedback is provided - generate config for all feedback types
                else:
                    # skip if not k=5
                    if env_config["max_steps"] != 5:
                        continue
                    for feedback_type in FEEDBACK_TYPES:
                        build_json_for_all_tasks(
                            agent_model_info=agent_model_info,
                            feedback_type=feedback_type,
                            feedback_model_info=feedback_model_info,
                            env_config=env_config,
                        )
