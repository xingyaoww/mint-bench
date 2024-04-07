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
    {
        "agent_class": "OpenAILMAgent",
        "config": {
            "model_name": "gpt-3.5-turbo-0613",
            "chat_mode": True,
            "max_tokens": 512,
            "temperature": 0.0,
        },
    },
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
    # {
    #     "agent_class": "ClaudeLMAgent",
    #     "config": {
    #         "model_name": "claude-instant-1",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #     },
    # },

    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Mistral-7B-Instruct-v0.2",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8000/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "zephyr-7b-beta",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8001/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "openchat-3.5-1210",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8002/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Starling-LM-7B-alpha",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8003/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Magicoder-S-DS-6.7B",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8004/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "OpenCodeInterpreter-DS-6.7B",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8005/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "MAmmoTH-7B-Mistral",
    #         "chat_mode": False,  # Cannot find its chat template
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8006/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "WizardMath-7B-V1.1",
    #         "chat_mode": False,  # Cannot find its chat template
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8007/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "OpenMath-Mistral-7B-v0.1-hf",
    #         "chat_mode": False,  # Cannot find its chat template
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8008/v1",
    #         "add_system_message": False,
    #     },
    # },

    # # ==== Larger ====
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Mixtral-8x7B-Instruct-v0.1",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8009/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "deepseek-coder-33b-instruct",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8010/v1",
    #         "add_system_message": False,
    #     },
    # },

    # # >67B
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "CodeLlama-70b-Instruct-hf",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8011/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "deepseek-llm-67b-chat",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8012/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Qwen1.5-72B-Chat",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8013/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "OpenCodeInterpreter-CL-70B",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8014/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "OpenMath-CodeLlama-70b-Python-hf",
    #         "chat_mode": False,  # Cannot find its chat template
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8015/v1",
    #         "add_system_message": False,
    #     },
    # }
    # ==== Eurus ====
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Eurus-7B-KTO",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8016/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Eurus-7B-SFT",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8017/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Eurus-70B-SFT",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8018/v1",
    #         "add_system_message": False,
    #     },
    # },
    # {
    #     "agent_class": "VLLMAgent",
    #     "config": {
    #         "model_name": "Eurus-70B-NCA",
    #         "chat_mode": True,
    #         "max_tokens": 512,
    #         "temperature": 0.0,
    #         "openai.api_base": "http://localhost:8019/v1",
    #         "add_system_message": False,
    #     },
    # },
]

FEEDBACK_PROVIDER_LIST = [
    {
        "agent_class": "None",
        "model_name": "None",
    },
    # NOTE: You can comment out the feedback provider you don't want to measure 
    # the ability of the evaluated model to leverage feedback
    # {
    #     "agent_class": "OpenAIFeedbackAgent",
    #     "model_name": "gpt-4-0613",
    # },
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
    # NOTE: You can comment out the feedback provider you don't want to measure 
    # the ability of the evaluated model to leverage feedback
    # {"pseudo_human_feedback": "no_GT", "feedback_form": "textual"},
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
