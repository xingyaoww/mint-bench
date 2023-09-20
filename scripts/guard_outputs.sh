#!/bin/bash
# Utility script to modify the outputs of the experiments

cmd=$1
destination_dir=$2  # e.g., data/outputs

if [ "$destination_dir" == "" ]; then
    echo "Usage: $0 [protect | unprotect] [destination_dir]"
    exit 1
fi

# if protect
if [ "$cmd" == "protect" ]; then
    find "$destination_dir" -type f -exec chmod 444 {} \;
    find "$destination_dir" -type d -exec chmod 555 {} \;
    echo "Write protection added to $destination_dir. Make all the files read-only."
else if [ "$cmd" == "unprotect" ]; then
    find "$destination_dir" -type f -exec chmod 744 {} \;
    find "$destination_dir" -type d -exec chmod 755 {} \;
    echo "Write protection removed. You can now delete the files if needed."
else
    echo "Usage: $0 [protect | unprotect]"
fi
fi
