#!/bin/bash

mkdir -p data
echo "=== 1. Setup all data ==="
PROCESSED_DATA_V1_URL="https://uofi.box.com/shared/static/xomunc5sddp3flbbkrog11xc6oy63soz"
if [ ! -d "data/processed" ]; then
    curl -L $PROCESSED_DATA_V1_URL --output data/processed-v1.zip
    unzip data/processed-v1.zip -d data

    # Count number of lines in each file while also accumulating the total number of lines
    TOTAL_LINES=0

    # - AlfWorld
    NUM_LINES=$(find data/processed/alfworld/ -name gt_traj.txt | wc -l)
    echo "AlfWorld: $NUM_LINES"
    TOTAL_LINES=$((TOTAL_LINES + NUM_LINES))

    # - All other datasets
    for file in $(find data/processed -name test_prompts.json); do
        NUM_LINES=$(wc -l $file | awk '{print $1}')
        echo "$file: $NUM_LINES"
        TOTAL_LINES=$((TOTAL_LINES + NUM_LINES))
    done

    echo "Total: $TOTAL_LINES"
    if [ $TOTAL_LINES -ne 586 ]; then
        echo "ERROR: Total number of lines is not 586! Some data is missing. Please raise an issue on GitHub!"
        exit 1
    fi
    rm data/processed-v1.zip
    echo "=== Data setup complete ==="
else
    echo "Data data/processed already exists. Skipping... Please delete the data folder if you want to re-download the data"
fi

echo "=== 2. Download existing LLM outputs ==="
OUTPUT_V1_URL="https://uofi.box.com/shared/static/a2p2tp4q6rmb2mfuim3fv3ff80ud8z2x"
if [ ! -d "data/outputs" ]; then
    curl -L $OUTPUT_V1_URL --output data/outputs-v1-release.zip
    unzip data/outputs-v1-release.zip -d data
    mv data/outputs-v1-release data/outputs
    rm data/outputs-v1-release.zip
    echo "=== Outputs setup complete ==="
else
    echo "Outputs data/outputs already exist. Skipping... Please delete the outputs folder if you want to re-download the outputs"
fi
