#!/bin/bash

set -e

ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N ""

# Run the command provided
exec "$@"

