#!/bin/bash

set -e

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

