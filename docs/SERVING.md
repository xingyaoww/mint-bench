# :wrench: Serving Open-Sourced Models

We use [VLLM](https://vllm.ai/) and [FastChat](https://github.com/lm-sys/FastChat/tree/main/fastchat) to serve open-source models. We prepare [nvidia-docker images](https://github.com/xingyaoww/llm-serving-hub/tree/main/docker) for all the serving.

Please refer to the documentation of [VLLM](https://vllm.ai/) and [FastChat](https://github.com/lm-sys/FastChat/tree/main/fastchat) if you do *not* wish to use docker for serving.

## Prepare your model

Download the model you want to evaluate from Huggingface.

```bash
cd $DIR_TO_SAVE_MODELS
git lfs install
git clone git@hf.co:<MODEL ID> # example: git clone git@hf.co:meta-llama/Llama-2-13b-chat-hf
```

## `VLLM`

We use VLLM to serve all open-source LLMs we evaluated, except CodeLLaMA, due to a [bug](https://github.com/vllm-project/vllm/issues/1001).

Please modify [`scripts/serve/run_vllm_serve.sh`](scripts/serve/run_vllm_serve.sh) to serve an huggingface-compatible model. You can modify the following settings in the script:

- `MODEL_DIR` (required): set this to your `$DIR_TO_SAVE_MODELS`.
- `MODEL_NAME` (required): name of your model (e.g., `Llama-2-13b-chat-hf` if you run `git clone git@hf.co:meta-llama/Llama-2-13b-chat-hf` in the previous step).
- `N_GPUS` (required): Number of GPUs you would like to use for tensor parallel
- `CUDA_VISIBLE_DEVICES` (required): GPU IDs, separated by a comma, that you want to use. For example, `0,1,2,3`.
- `PORT` (optional): The port you want to serve your LLM.

After you set all the above correctly, you can run `scripts/serve/run_vllm_serve.sh` to spin up a server with OpenAI-compatible API, available at `http://localhost:$PORT`.

You can test whether the server is successfully started by running:

```bash
curl http://localhost:$PORT/v1/models
```

NOTE: we renamed the clone model name for [lemur-chat model](https://huggingface.co/OpenLemur/lemur-70b-chat-v1) by doing: `mv lemur-70b-chat-v1 llama-2-lemur-70b-chat-v1` since VLLM and FastChat use this [directory name to match the corresponding chat template](https://github.com/lm-sys/FastChat/blob/3149253988ee16b0945aa0a381a42a07b8a7829e/fastchat/model/model_adapter.py#L1257).


## `FastChat`

We serve all the [CodeLLaMA models](https://huggingface.co/codellama) using `scripts/serve/run_fastchat_serve.sh`. The variables that need to be configured are the same as VLLM above.


## FAQ

**What if the GPU server (server-A) I have access to for model serving does not have access to the Internet for API-based feedback-provider? I have another machine without a GPU that has access to the Internet (server-B).**

First, make sure that you can `ssh` from `server-A` to `server-B`.

Then you can use `ssh`'s built-in proxy functionality by running:

```bash
# on server-A
ssh -N -L 0.0.0.0:$PORT:localhost:$PORT server-B

# If you installed autossh (recommended) that allows for automatic reconnection, you can replace the above command with the following:
autossh -M 0 -N -L 0.0.0.0:$PORT:localhost:$PORT server-B
```

Then you should be able to access the LLM served by VLLM or FastChat on `server-B`:
```bash
# on server-B
curl http://localhost:$PORT/v1/models
```
