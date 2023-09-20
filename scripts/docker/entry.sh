#!/bin/bash
# NOTE: This is expected to be execute inside the docker container

# Set up a user with the provided user ID
USERNAME=mint
useradd --shell /bin/bash -u $HOST_USER_ID -o -c "" -m $USERNAME
ulimit -n 4096
su $USERNAME
