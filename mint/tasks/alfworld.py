import os
import yaml
import logging
from typing import Iterable
import alfworld
import alfworld.agents.environment as envs
import json
import os

LOGGER = logging.getLogger("MINT")

from mint.tasks.base import Task

PREFIXES = {
    "pick_and_place": "put",
    "pick_clean_then_place": "clean",
    "pick_heat_then_place": "heat",
    "pick_cool_then_place": "cool",
    "look_at_obj": "examine",
    "pick_two_obj": "puttwo",
}


class AlfWorldTask(Task):
    """Alfworld task instance."""

    task_name = "alfworld"

    def __init__(
        self,
        id: str,
        prompt: str,
        reference: str,
        env: envs.AlfredTWEnv,
        task_type: str,
        **kwargs,
    ):
        self.task_name = f"alfworld/{task_type}"  # used to load the correct ICL example
        super().__init__(**kwargs)
        self._id = id
        self._prompt = prompt.strip()
        self._reference = reference
        self.metadata["task_type"] = task_type

        # NOTE: AlfWorld is different -> no reference solution
        self._env = env

    @property
    def env(self) -> envs.AlfredTWEnv:
        """Stateful environment of the task.

        Specific for AlfWorld.
        """
        return self._env

    def success(self, solution: str) -> bool:
        """This checks whether the given solution can complete the current task."""
        # Task success is checked at the environment level, not at the solution level.
        raise NotImplementedError

    @classmethod
    def load_tasks(cls, path: str = "./data/processed/alfworld") -> Iterable["Task"]:
        """Load alfworld data and prompts from a directory."""

        with open(os.path.join(path, "base_config.yaml")) as f:
            config = yaml.safe_load(f)

        # Split following ReAct
        # https://github.com/ysymyth/ReAct/blob/master/alfworld.ipynb
        split = "eval_out_of_distribution"
        env = getattr(alfworld.agents.environment, config["env"]["type"])(
            config, train_eval=split
        )
        assert isinstance(env, alfworld.agents.environment.AlfredTWEnv)
        env = env.init_env(batch_size=1)

        N_TASKS = 134  # as hardcoded in ReAct

        def generator():
            loaded_history_path = os.path.join(
                os.path.dirname(path), "test_prompts.json"
            )
            if os.path.exists(loaded_history_path):
                loaded_histories = [
                    json.loads(i) for i in open(loaded_history_path).readlines()
                ]
                loaded_histories = {
                    i["prompt"].strip(): i["loaded_history"] for i in loaded_histories
                }
            else:
                loaded_histories = None

            for _ in range(N_TASKS):
                ob, info = env.reset()
                ob = "\n".join(ob[0].split("\n\n")[1:])
                game_file = info["extra.gamefile"][0]
                gt_reference_file = os.path.join(
                    os.path.dirname(game_file), "gt_traj.txt"
                )

                with open(gt_reference_file) as f:
                    gt_reference = f.read()

                name = "/".join(game_file.split("/")[-3:-1])
                LOGGER.info(f"Loaded task {name} from {split} split.")

                task_type = None
                for _, (k, v) in enumerate(PREFIXES.items()):
                    if name.startswith(k):
                        task_type = v
                        break
                assert task_type is not None, f"Task type not found for {name}"

                prompt = "Interact with a household to solve a task. \n" + ob
                if loaded_histories == None:
                    yield cls(
                        id=name,
                        prompt=prompt,
                        reference=gt_reference,
                        env=env,
                        task_type=task_type,
                        loaded_history=None,
                    )
                else:
                    if prompt.strip() in loaded_histories:
                        loaded_history = loaded_histories[prompt]
                        yield cls(
                            id=name,
                            prompt=prompt,
                            reference=gt_reference,
                            env=env,
                            task_type=task_type,
                            loaded_history=loaded_history,
                        )
                    else:
                        LOGGER.info("NO LOADED HISTORY FOUND")
                        continue

        return generator(), N_TASKS
