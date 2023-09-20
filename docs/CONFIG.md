
# :paperclip: How to configure MINT to evaluate your LLM

## Add an evaluated LLM

MINT use different class to abstract out the API of different LLMs. You can find the list of implemented LLMs in [`mint/agents/__init__.py`](mint/agents/__init__.py).

For closed-source models:
- [`OpenAILMAgent`](mint/agents/openai_lm_agent.py) for [OpenAI API](https://platform.openai.com/docs/api-reference).
- [`BardLMAgent`](mint/agents/bard_agent.py) for [Bard](https://www.googlecloudcommunity.com/gc/AI-ML/Google-Bard-API/m-p/538517).
- [`ClaudeLMAgent`](mint/agents/claude_agent.py) for [Anthropic Claude](https://docs.anthropic.com/claude/docs/getting-access-to-claude).

For open-source models, we have [`VLLMAgent`](mint/agents/vllm_agent.py) that can be used to evaluate any LLMs that can be served with [VLLM](https://vllm.ai/) or [FastChat](https://github.com/lm-sys/FastChat/tree/main/fastchat) into an OpenAI-compatible API.

**If you want to evaluate an open-source LLM that can be served with VLLM or FastChat**: First, refer to [`docs/SERVING.md`](../docs/SERVING.md) to learn about how to serve your model. Then, modify [`mint/configs/config_variables.py`](mint/configs/config_variables.py) by adding a dictionary describing the model to be evaluated into `EVALUATED_MODEL_LIST`.

```python
# For Chat Model
{
    "agent_class": "VLLMAgent",
    "config": {
        "model_name": "<YOUR_MODEL_NAME>",
        "chat_mode": True,
        "max_tokens": 512,
        "temperature": 0.0,
        "openai.api_base": "<YOUR_API_BASE>",
        "add_system_message": False,
    },
}
# For Completion-only Model
{
    "agent_class": "VLLMAgent",
    "config": {
        "model_name": "Llama-2-70b-hf",
        "chat_mode": False,
        "max_tokens": 512,
        "temperature": 0.0,
        "openai.api_base": "<YOUR_API_BASE>",
        "add_system_message": False,
    },
},
```

**If you want to evaluate another closed-source LLM with a different API schema than the existing implementation**: You need to implement a new agent class that inherits from `LMAgent` (PR welcomed!).
You can use [`mint/agents/openai_lm_agent.py`](mint/agents/openai_lm_agent.py) as an example, then add this model configuration to [`mint/configs/config_variables.py`](mint/configs/config_variables.py) similar to the above.


## Add a feedback-providing LLM

We implemented three different feedback agent classes:
- [OpenAIFeedbackAgent](mint/agents/openai_feedback_agent.py)
- [ClaudeFeedbackAgent](mint/agents/claude_feedback_agent.py)
- [VLLMFeedbackAgent](mint/agents/vllm_feedback_agent.py)

If you want to use an existing open-source model compatible with VLLM or FastChat, you can add a configuration similar to the above to `FEEDBACK_PROVIDER_LIST` in [`mint/configs/config_variables.py`](mint/configs/config_variables.py).

```python
FEEDBACK_PROVIDER_LIST = [
    ...
    {
        "agent_class": "VLLMFeedbackAgent",
        "model_name": "<YOUR_MODEL_NAME>",
        "openai.api_base": "<YOUR_API_BASE>",
        "chat_mode": True, # Set to False if your model is completion-only
    },
    ...
]
```

If needed, you can use these classes as an example to implement your own feedback agent class (PR welcomed!). Then, add this model configuration to `FEEDBACK_PROVIDER_LIST` in [`mint/configs/config_variables.py`](mint/configs/config_variables.py). For example:

```python
FEEDBACK_PROVIDER_LIST = [
    ...
    {
        # Your custom feedback provider
        "agent_class": "<YOUR_FEEDBACK_AGENT_CLASS>",
        "model_name": "<YOUR_FEEDBACK_MODEL_NAME>",
    },
    ...
]
```


## Change Experiment Configurations

Optionally, you can change different experiment settings in [`mint/configs/config_variables.py`](mint/configs/config_variables.py).

### `ENV_CONFIGS`

This specifies the settings of the environment. Here is an example:

```python
ENV_CONFIGS = [
    ...,
    {
        "max_steps": 5,
        "use_tools": True,
        "max_propose_solution": 2,
        "count_down": True,
    },
    ...
]
```

where `max_steps` corresponds to the budget of interaction (k) in the paper, `use_tools` should always be `True` (no tool setting is not implemented yet), `max_propose_solution` is the maximum number of solutions that the evaluated LLM can propose, and `count_down` is whether to count down the remaining steps in the environment (read Section 2 in the paper for more detail).

### `FEEDBACK_TYPES`

This specifies the types of feedback we instruct the feedback-providing LLM to provide. Here are all the settings we currently support:

```python
FEEDBACK_TYPES = [
    {"pseudo_human_feedback": "no_GT", "feedback_form": "textual"}, # default setting
    {"pseudo_human_feedback": "no_GT", "feedback_form": "binary"},
    {"pseudo_human_feedback": "GT", "feedback_form": "binary"},
    {"pseudo_human_feedback": "GT", "feedback_form": "textual"},
]
````

- `pseudo_human_feedback` specifies whether we provide a ground-truth solution of the problem to the feedback-providing LLM. `no_GT` means we do not provide a ground-truth solution (default setting), and `GT` means we provide ground-truth feedback.
- `feedback_form` specifies the form of feedback we provide. `textual` means we provide textual feedback (default setting), and `binary` means we instruct the feedback-provider to provide binary feedback.
