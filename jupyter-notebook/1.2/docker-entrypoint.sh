#!/bin/bash

set -e

# If the run command is the default, do some initialization first
if [ "$(which "$1")" = "/usr/local/bin/start-singleuser.sh" ]; then
  gitpuller https://github.com/fabric-testbed/jupyter-examples master example-notebooks
fi

# Run the command provided
exec "$@"

mkdir $HOME/.ssh/
ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N ""

mkdir -p $WORKDIR/.ssh/
FILE=$WORKDIR/.ssh/id_rsa

if [[ ! -f "$FILE" ]]; then
    cp $HOME/.ssh/id_rsa $WORKDIR/.ssh/
    cp $HOME/.ssh/id_rsa.pub $WORKDIR/.ssh/
fi

