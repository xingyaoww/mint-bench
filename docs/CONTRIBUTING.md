# :star2: Contribute

We welcome the community's contribution to making this benchmark more comprehensive and challenging as LLMs get better.

## Contribute Tools

MINT implements a series of tools and allows LMs to interact with them through Python Code execution. The tools can be found in `mint/tools`.
We provide full implementations for the three main types of tools we used in our paper.

- [`PythonREPL`](mint/tools/python_tool.py), this tool implements an interface to execute Python code based on IPython, and it is the primary interface for LLM to leverage tools.
- [`WikipediaQueryRun`](mint/tools/wikipedia_search.py) for executing a wikipedia search.
- [`AlfWorldTool`](mint/tools/alfworld.py), this tool is a base tool for all actions available in a sequential decision-making task [Alfworld](https://github.com/alfworld/alfworld).
We inherit nine different types of 'specific action' tools from this base tool, which are "Put, Goto, Clean, Close, Open, Heat, Cool, Toggle, Take."
For example, if the LM agent wants to take an apple from the table, it can call the Take Tool and pass (apple, table) as its argument.

To contribute new tools under this setting, you need to implement a tool class inherited from [`Tool`](mint/tools/base.py) with the following class variable and methods:

Class variables:

You need to provide three properties, which are the `name`, `signature`, and `description` for the tools you created. All of these variable are strings. Remember to keep the 'name' variable unique, and you can provide and descriptions and signatures template for the tool, which will be exposed to the LLM through `get_toolset_description` function in [`mint/tools/__init__.py`](mint/tools/__init__.py).

Methods:

You only need to implement the `__call__()` function for each tool, which should finally return a text output as the observation that LLM received after executing the tool.
You may also need to implement custom changes if you are using a stateful tool; check our implementation for [Alfworld](mint/tools/alfworld.py) and [its environment](mint/envs/alfworld_env.py) as an example.

## Contribute Dataset

You can contribute a custom dataset comprising tasks you found important for LMs to interact with. Note that good tasks for our evaluation setting should be relatively hard and LMs may need multi-turn interactions with the environment or feedback to get to the final solution.

### Prepare Your Dataset in the unified format

You should prepare your dataset and generate a `test_prompts.json` (a JSON Line file) with three required keys, namely `id`, `prompt`, and `reference`. The `prompt` should be a question or instruction that is provided to the LM, while the `reference` is the ground truth for your task, that may or may not be used in later defined task class. You can put this `test_prompts.json` under `data/processed/<YOUR_TASK_NAME>`.

You can use `scripts/setup.sh` to download our processed data as examples and check our data format.

### Implement a Task Class

To add a task that LLM will be able to execute with multi-turn interactions, you first need to implement a task class inherited from [`Task`](mint/tasks/base.py) with the following class variables and methods:

Class variables:

- `task_name`: This specifies a name for each independent task.
- `in_context_example_dir`: The default in-context-example directory. You can provide a few shot examples for this task by adding context examples.
Please check `mint/tasks/in_context_examples` for examples.

Methods you should implement:

- `success(solution: str) -> bool`: Providing a solution string from the LM, check valid whether the answer is successful.

- `load_tasks(cls, path: str) -> Tuple[Iterable[Task], int]`: Providing the path that stores a data file, it returns a tuple of (the list of Task instances, number of total instances). You can first check our base implementation in `mint/tasks/base.py` to decide whether you want to implement your own `load_tasks`.

You can add any other features you want to build a task class; refer to our example of [code generation](mint/tasks/codegen.py) or [Alfworld Task](mint/tasks/alfworld.py) for reference.

### Add your task to the config

Modify `TASK_INFO_MAP` in [`mint/configs/config_variables.py`](mint/configs/config_variables.py). Also modify `TASK_TYPE_TO_TOOL_IMPORT` if you want to include tools associated with this task.

- `TASK_INFO_MAP`: Map `task_name` to `{"class": "YourTaskClass", "type": "TASK_TYPE"}`.
- `TASK_TYPE_TO_TOOL_IMPORT`: Map generic `TASK_TYPE` to `List[Tool]``.

Please check [docs/CONFIG.md](../docs/CONFIG.md) for more config details.

## Submit a PR!

You can submit a PR with your implemented task class, data instances (in `data/processed`), and updated [`mint/configs/config_variables.py`](mint/configs/config_variables.py).
