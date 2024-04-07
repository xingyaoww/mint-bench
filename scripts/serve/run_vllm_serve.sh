#!/bin/bash
DOCKER_IMG="vllm/vllm-openai"

# Model directory: contains model (cloned) downloaded from huggingface
# 1. git lfs install
# 2. git clone git@hf.co:<MODEL ID> # example: git clone git@hf.co:meta-llama/Llama-2-13b-chat-hf
# MODEL_DIR="<YOUR_MODEL_DIR>" # e.g., dir that contains Llama-2-13b-chat-hf
# MODEL_NAME="Llama-2-13b-chat-hf"
MODEL_DIR="/shared/nas2/shared/llms" # e.g., dir that contains Llama-2-13b-chat-hf
MODEL_NAME=$1
NUM_BATCHED_TOKENS=16384

if [ -z "$MODEL_NAME" ]; then
    echo "Usage: $0 <model_name> <port>"
fi
PORT=$2
if [ -z "$PORT" ]; then
    echo "Usage: $0 <model_name> <port>"
fi

# Set CUDA_VISIBLE_DEVICES to the GPU ids you want to use.
# If you have multiple GPUs, you can use this to control which GPUs are used.
if [ -z "$CUDA_VISIBLE_DEVICES" ]; then
    echo "CUDA_VISIBLE_DEVICES is not set. Please set CUDA_VISIBLE_DEVICES to the GPU ids you want to use."
    exit 1
fi

echo "NUM_BATCHED_TOKENS set to $NUM_BATCHED_TOKENS by default. Please change if needed."
export N_GPUS=$(echo $CUDA_VISIBLE_DEVICES | tr ',' '\n' | wc -l)


# Construct instance name using the current username and the current time.
# This is useful for running multiple instances of the docker container.
DOCKER_INSTANCE_NAME="vllm_${USER}_${MODEL_NAME}_PORT_${PORT}_$(date +%Y%m%d_%H%M%S)"

echo "==================="
echo "DOCKER_IMG: $DOCKER_IMG"
echo "DOCKER_INSTANCE_NAME: $DOCKER_INSTANCE_NAME"
echo "MODEL_DIR: $MODEL_DIR"
echo "MODEL_NAME: $MODEL_NAME"
echo "PORT: $PORT"
echo "CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"
echo "N_GPUS: $N_GPUS"
echo "==================="

docker run \
    -e CUDA_VISIBLE_DEVICES \
    -v $MODEL_DIR:/home/vllm/model/ \
    --net=host --rm --gpus all \
    --shm-size=64g \
    --name $DOCKER_INSTANCE_NAME \
    $DOCKER_IMG \
    --model /home/vllm/model/$MODEL_NAME \
    --tensor-parallel-size $N_GPUS \
    --served-model-name $MODEL_NAME \
    --max-num-batched-tokens $NUM_BATCHED_TOKENS \
    --enforce-eager \
    --host 0.0.0.0 \
    --port $PORT
