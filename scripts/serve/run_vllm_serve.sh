export HOST_USER_ID=$(id -u)
DOCKER_IMG="xingyaoww/vllm:v1.1.1"

# Model directory: contains model (cloned) downloaded from huggingface
# 1. git lfs install
# 2. git clone git@hf.co:<MODEL ID> # example: git clone git@hf.co:meta-llama/Llama-2-13b-chat-hf
MODEL_DIR="<YOUR_MODEL_DIR>" # e.g., dir that contains Llama-2-13b-chat-hf
MODEL_NAME="Llama-2-13b-chat-hf"
PORT=8000

# Construct instance name using the current username and the current time.
# This is useful for running multiple instances of the docker container.
DOCKER_INSTANCE_NAME="vllm_${USER}_${MODEL_NAME}_$(date +%Y%m%d_%H%M%S)"

# Set CUDA_VISIBLE_DEVICES to the GPU ids you want to use.
# If you have multiple GPUs, you can use this to control which GPUs are used.
export N_GPUS=4
export CUDA_VISIBLE_DEVICES=0,1,2,3

docker run \
    -e CUDA_VISIBLE_DEVICES \
    -v $MODEL_DIR:/home/vllm/model/ \
    --net=host --rm --gpus all \
    --shm-size=10.24gb \
    --name $DOCKER_INSTANCE_NAME \
    $DOCKER_IMG \
    bash -c "
    useradd --shell /bin/bash -u $HOST_USER_ID -o -c "" -m vllm; su vllm;
    python3 -m vllm.entrypoints.openai.api_server \
    --model /home/vllm/model/$MODEL_NAME \
    --tensor-parallel-size $N_GPUS \
    --served-model-name $MODEL_NAME \
    --max-num-batched-tokens 4096 \
    --load-format pt \
    --host 0.0.0.0 \
    --port $PORT
    "


# Example usage for MODEL_NAME=Llama-2-13b-chat-hf
# curl http://localhost:8000/v1/completions -H "Content-Type: application/json" -d '{
#   "model": "Llama-2-13b-chat-hf",
#   "prompt": "San Francisco is a",
#   "max_tokens": 7,
#   "temperature": 0
# }'
