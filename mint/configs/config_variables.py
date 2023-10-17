# all configs are flexible to adapt with this config_variables.py
# if you want to change data output dir or dataset dir, please change DATA_OUTPUTS_DIR and DATASET_DIR
# if you want to add more configs, please:
# (1) if you want to add tools, please add to TASK_TYPE_TO_TOOL_IMPORT
# (2) if you want to add tasks, please add to TASK_INFO_MAP
# (3) if you want to add agent models, please add to agent_model_infos
# (4) if you want to add feedback models and configs, please add to feedback_model_infos and feedback_types
# (5) if you want to add env configs, please add to env_configs

DATA_OUTPUTS_DIR = "data/outputs"
DATASET_DIR = "data/processed"

TASK_TYPE_TO_TOOL_IMPORT = {
    "reasoning": [("mint.tools.wikipedia_search", "WikipediaQueryRun")],
    "decision_making": [],
    "code_generation": [],
}

TASK_INFO_MAP = {
    # === Reasoning ===
    "theoremqa": {"class": "TheoremqaTask", "type": "reasoning"},
    "gsm8k": {"class": "ReasoningTask", "type": "reasoning"},
    "hotpotqa": {"class": "ReasoningTask", "type": "reasoning"},
    "mmlu": {"class": "MultipleChoiceTask", "type": "reasoning"},
    "math": {"class": "ReasoningTask", "type": "reasoning"},
    # === Code Generation ===
    "mbpp": {
        "class": "MBPPTask",
        "type": "code_generation",
    },
    "humaneval": {
        "class": "HumanEvalTask",
        "type": "code_generation",
    },
    # === Decision Making ===
    "alfworld": {"class": "AlfWorldTask", "type": "decision_making"},
}

FEEDBACK_CONFIG = {
    "feedback_agent_config": {
        "chat_mode": True,
        "max_tokens": 1024,
        "temperature": 0.0,
        "stop": ["\nQ:"],
    }
}

EVALUATED_MODEL_LIST = [
    # {
    #     "agent_class": "OpenAILMAgent",
    #     "config": {
    #         "model_name": "gpt-3.5-turbo-0613",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #     },
    # },
    # {
    #     "agent_class": "OpenAILMAgent",
    #     "config": {
    #         "model_name": "gpt-3.5-turbo-16k-0613",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #     },
    # },
    # {
    #     "agent_class": "OpenAILMAgent",
    #     "config": {
    #         "model_name": "gpt-4-0613",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #     },
    # },
    # Bard
    # {
    #     "agent_class": "BardLMAgent",
    #     "config": {
    #         "model_name": "chat-bison-001",
    #         "add_system_message": False,
    #         "temperature": 0.0,
    #         "candidate_count": 1,
    #     },
    # },
    # LLaMA2
    # {
    #     "agent_class": "LLaMA2LMAgent",
    #     "config": {
    #         "model_name": "Llama-2-7b-chat-hf",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    # },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Llama-2-7b-hf",
    #         "chat_mode": False,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Llama-2-13b-hf",
    #         "chat_mode": False,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Llama-2-70b-hf",
    #         "chat_mode": False,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Llama-2-7b-chat-hf",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Llama-2-13b-chat-hf",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Llama-2-70b-chat-hf",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "llama-2-lemur-70b-chat-v1",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "llama-2-lemur-70b-v1",
    #         "chat_mode": False,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "vicuna-7b-v1.5",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "vicuna-13b-v1.5",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "vicuna-7b-v1.5-16k",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "vicuna-13b-v1.5-16k",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "CodeLlama-7b-hf",
    #         "chat_mode": False,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "CodeLlama-13b-hf",
    #         "chat_mode": False,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "CodeLlama-34b-hf",
    #         "chat_mode": False,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "CodeLlama-7b-Instruct-hf",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "CodeLlama-13b-Instruct-hf",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "CodeLlama-34b-Instruct-hf",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "<YOUR_API_BASE>",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "ClaudeLMAgent",
    #     "config": {
    #         "model_name": "claude-2",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #     },
    # },
    {
        "agent_class": "ClaudeLMAgent",
        "config": {
            "model_name": "claude-instant-1",
            "chat_mode": True,
            "max_tokens": 512,
            "temperature": 0.0,
        },
    },
]

FEEDBACK_PROVIDER_LIST = [
    {
        "agent_class": "None",
        "model_name": "None",
    },
    {
        "agent_class": "OpenAIFeedbackAgent",
        "model_name": "gpt-4-0613",
    },
    # {
    #     "agent_class": "OpenAIFeedbackAgent",
    #     "model_name": "gpt-3.5-turbo-16k-0613",
    # },
    # {
    #     "agent_class": "ClaudeFeedbackAgent",
    #     "model_name": "claude-2",
    # },
    # {
    #     "agent_class": "ClaudeFeedbackAgent",
    #     "model_name": "claude-instant-1",
    # },
    # {
    #     "agent_class": "VLLMFeedbackAgent",
    #     "model_name": "Llama-2-70b-chat-hf",
    #     "openai.api_base": "<YOUR_API_BASE>",
    #     "chat_mode": True,
    # },
    # {
    #     "agent_class": "VLLMFeedbackAgent",
    #     "model_name": "CodeLlama-34b-hf",
    #     "openai.api_base": "<YOUR_API_BASE>",
    #     "chat_mode": False,
    # },
    # {
    #     "agent_class": "VLLMFeedbackAgent",
    #     "model_name": "Llama-2-70b-hf",
    #     "openai.api_base": "<YOUR_API_BASE>",
    #     "chat_mode": False,
    # },
    # {
    #     "agent_class": "VLLMFeedbackAgent",
    #     "model_name": "CodeLlama-34b-Instruct-hf",
    #     "openai.api_base": "<YOUR_API_BASE>",
    #     "chat_mode": False,
    # },
]

FEEDBACK_TYPES = [
    {"pseudo_human_feedback": "no_GT", "feedback_form": "textual"},
    # {"pseudo_human_feedback": "no_GT", "feedback_form": "binary"},
    # {"pseudo_human_feedback": "GT", "feedback_form": "binary"},
    # {"pseudo_human_feedback": "GT", "feedback_form": "textual"},
]

ENV_CONFIGS = [
    {
        "max_steps": 5,
        "use_tools": True,
        "max_propose_solution": 2,
        "count_down": True,
    },
    {
        "max_steps": 4,
        "use_tools": True,
        "max_propose_solution": 2,
        "count_down": True,
    },
    {
        "max_steps": 3,
        "use_tools": True,
        "max_propose_solution": 2,
        "count_down": True,
    },
    {
        "max_steps": 2,
        "use_tools": True,
        "max_propose_solution": 2,
        "count_down": True,
    },
    {
        "max_steps": 1,
        "use_tools": True,
        "max_propose_solution": 1,
        "count_down": True,
    },
    # {
    #     "max_steps": 6,
    #     "use_tools": True,
    #     "max_propose_solution": 2,
    #     "count_down": True,
    # },
    # {
    #     "max_steps": 8,
    #     "use_tools": True,
    #     "max_propose_solution": 2,
    #     "count_down": True,
    # },
    # {
    #     "max_steps": 10,
    #     "use_tools": True,
    #     "max_propose_solution": 2,
    #     "count_down": True,
    # }
]
