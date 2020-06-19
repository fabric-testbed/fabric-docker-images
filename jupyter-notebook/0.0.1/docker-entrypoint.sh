#!/bin/bash

set -e

# If the run command is the default, do some initialization first
if [ "$(which "$1")" = "/usr/local/bin/start-singleuser.sh" ]; then
  gitpuller https://github.com/fabric-testbed/jupyternb-template master template
fi

# Run the command provided
exec "$@"

