#!/bin/bash

# this is a script that helps migrate Neo4j database from 4.1.6 to 5.3.0

# Overall the process involves dumping the neo4j database in 4.1.6
# (current version) in SF4.0.0 format, then ingesting it inside an intermediate
# neo4j 4.4.16 to convert to SF4.3.0 and dumping again to then ingest in neo4j
# 5.3.0 and issuing explicit migrate command. Note that neo4j-admin extensively
# used here changed its features between neo4j 4.x and neo4j 5.x.

#
# Some definitions
#

# operations
OPTS=`getopt -o ih -n migrate.sh -- "$@"`

INTERACTIVE=0
UNDO=0

while true; do
  case "$1" in
    -i ) INTERACTIVE=1; shift 1;;
    -u ) UNDO=1; echo "Attempt to undo and put everything back to 4.1.6 can work"; shift 1;;
    -h ) echo -e "This script migrates Neo4j graph database contents from 4.1.6/SF4.00 (via 4.4.16/SF4.3.0) to 5.3.0/SF5.x. \n Use -i to force prompted interactive mode. \n Use -u to try to put things back as they were."; exit 0;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

# Neo4j containers
neo4j_416="fabrictestbed/neo4j-apoc:4.1.6"
neo4j_4416="neo4j:4.4.16-community"
neo4j_530="neo4j-fabric"

neo4j_416_name="neo4j-orig"
neo4j_4416_name="neo4j-interim"
neo4j_530_name="neo4j-final"

# starting a container
container_start_prefix="docker run -d   --user=$(id -u):$(id -g)  --publish=7473:7473   --publish=7474:7474   --publish=7687:7687   --volume=$(pwd)/neo4j/data:/data   --volume=$(pwd)/neo4j/imports:/imports -e NEO4J_AUTH=neo4j/password"
container_exec_prefix="docker exec -ti ${_cont_name} "
container_stop="docker container stop ${_cont_name}"
container_remove="docker container rm ${_cont_name}"

# set to 0 if you want to skip the prompts
interactive=1

# name of dump file. note that Neo4j 4.1 and 4.4 expect the file to be named
# same as database so this cannot be changed to e.g. neo4j-4.1.6.dump
dumpfile="./neo4j/imports/neo4j.dump"
dumpfile4416="./neo4j/imports/neo4j-4.4.16.dump"
dumpcopy416="./neo4j-4.1.6.dump"
dumpcopy4416="./neo4j-4.4.16.dump"

function start_neo4j
{
  local _cont_name="${1}"
  local _img_name="${2}"
  local _options="${3}"

  if [ ! -d ./neo4j/data ]; then
    error_msg "./neo4j/data directory is missing"
  fi
  echo "- Starting container ${_img_name} as ${_cont_name} with options ${_options}..."
  eval ${container_start_prefix} --name=${_cont_name} ${_options} ${_img_name}
  sleep 10
}

function start_neo4j_bash
{
  local _cont_name="${1}"
  local _img_name="${2}"

  if [ ! -d ./neo4j/data ]; then
    error_msg "./neo4j/data directory is missing"
  fi
  echo "- Starting container ${_img_name} as ${_cont_name} with bash..."
  eval ${container_start_prefix} --name=${_cont_name} -it ${_img_name} /bin/bash
  sleep 10
}

function execute_container_command
{
  local _cont_name="${1}"
  local _cmd="${2}"

  echo "- Executing command ${_cmd} on container ${_cont_name}"
  eval ${container_exec_prefix} ${_cont_name} ${_cmd}
}

function stop_and_remove_container
{
  local _cont_name="${1}"

  echo "- Stopping and removing container image ${_cont_name}"
  eval ${container_stop} ${_cont_name} >& /dev/null
  eval ${container_remove} ${_cont_name} >& /dev/null
}

function pause_and_prompt
{
  local _prompt="${1}"

  if [[ $INTERACTIVE -eq 1 ]]; then
    echo ${_prompt}
    echo -n "Press ENTER"
    read -n 1
  fi
}

function error_msg
{
  local _error_msg="${1}"

  echo "*** An error has occurred: ${_error_msg}, exiting"
  exit -1
}

function create_neo4j_backup
{
  # tar and save backup of neo4j/ directory structure
  local _backup_name="${1}"
  local _remove="${2}"
  if [ ! -d ./neo4j ]; then
    error "Unable to find ./neo4j directory, perhaps not executing from the right location."
  fi

  echo "- Backing neo4j database up to ${_backup_name}.tar.gz"
  tar -cf ${_backup_name}.tar.gz neo4j/
  if [[ $_remove = "1" ]]; then
    echo "- Removing old neo4j data"
    rm -rf ./neo4j/data ./neo4j/logs
  fi
}

function initialize_state
{
  stop_and_remove_container neo4j
  stop_and_remove_container neo4j-4416
  stop_and_remove_container neo4j-bash
  stop_and_remove_container neo4j-4416-bash
  stop_and_remove_container neo4j-530-bash
}
#
# Main sequence of the script
#
if [ $UNDO -eq 1 ]; then
  pause_and_prompt "- Attempting to undo the script by stopping removing any stale containers and putting the data back"
  initialize_state
  if [ -f ./neo4j-416.tar.gz ]; then
    echo "- Restoring data from tar"
    rm -rf neo4j/data
    tar -zxf ./neo4j-416.tar.gz
  else
    echo "Unable to restore database data - tar file neo4j-416.tar.gz missing"
    exit -1
  fi
  exit 0
fi

let step=0

pause_and_prompt "We assume that Neo4j 4.1.6 *was* running and is now stopped. We assume you are running this script from just above the neo4j/ folder."
if [ ! -d ./neo4j ]; then
  error_msg "You must be running from just above the ./neo4j folder."
fi
pause_and_prompt "Step ${step}. Remove old container images."
let step++
initialize_state

pause_and_prompt "We start by dumping data out of 4.1.6 file and placing it under ./neo4j/imports"

pause_and_prompt "Step ${step}. Start neo4j 4.1.6 container in bash mode and dump the data into ./neo4j/imports/neo4j.dump"
let step++
if [ -f ${dumpfile} ]; then
  echo "- Removing old dump file"
  rm -f ${dumpfile}
fi
start_neo4j_bash neo4j-bash ${neo4j_416}
execute_container_command neo4j-bash '/var/lib/neo4j/bin/neo4j-admin dump --database=neo4j --to=/imports/neo4j.dump'
if [ ! -f ${dumpfile} ]; then
  error_msg "Dumping the database failed, unable to find dump file"
fi
echo "- Dump file ${dumpfile} copied to current dir"
cp ${dumpfile} ${dumpcopy416}

pause_and_prompt "Step ${step}. Stop and remove neo4j-bash container"
let step++
stop_and_remove_container neo4j-bash

pause_and_prompt "Step ${step}. Backup neo4j database using tar and remove old data "
let step++
create_neo4j_backup neo4j-416 1

pause_and_prompt "Step ${step}. Create blank ./neo4j/data directory"
let step++
mkdir -p ./neo4j/data

pause_and_prompt "Next we will start Neo4j 4.4.16, import the dump into it to convert to SF4.3.0 from SF4.0.0 and create another dump"
pause_and_prompt "Step ${step}. Start 4.4.16 neo4j-bash container"
let step++
start_neo4j_bash neo4j-4416-bash ${neo4j_4416}

pause_and_prompt "Step ${step}. Import data from dump"
let step++
execute_container_command neo4j-4416-bash '/var/lib/neo4j/bin/neo4j-admin load --from=/imports/neo4j.dump --database=neo4j --force'

pause_and_prompt "Step ${step}. Shutdown neo4j bash container"
let step++
stop_and_remove_container neo4j-4416-bash

pause_and_prompt "Step ${step}. Run neo4j in container to force migration to new format."
let step++
start_neo4j neo4j-4416 ${neo4j_4416} '-e NEO4J_dbms_allow__upgrade=true'

pause_and_prompt "Step ${step}. Watch docker logs to make sure migration completes. The command terminates in 60 seconds, if migration is not completed, terminate the script."
let step++
timeout 60s docker logs -f neo4j-4416

stop_and_remove_container neo4j-4416

pause_and_prompt "Step ${step}. Start 4.4.16 container in bash mode again and dump in new format"
let step++
start_neo4j_bash neo4j-4416-bash ${neo4j_4416}
execute_container_command neo4j-4416-bash '/var/lib/neo4j/bin/neo4j-admin dump --database=neo4j --to=/imports/neo4j-4.4.16.dump'

if [ ! -f ${dumpfile4416} ]; then
  error_msg "Dumping the database in intermediate format failed, unable to find dump file"
fi
cp ${dumpfile4416} ${dumpcopy4416}

pause_and_prompt "Step ${step}. Shut down 4.4.16 bash container."
let step++
stop_and_remove_container neo4j-4416-bash

pause_and_prompt "The final phase involves using a 5.3.0 container to migrate to SF5.x.x"
pause_and_prompt "Step ${step}. We rename the ./neo4j/imports/dump-4.4.16.dump file into ./neo4j/imports/neo4j.dump"
let step++
mv ${dumpfile4416} ${dumpfile}

pause_and_prompt "Step ${step}. Save intermediate data in tar and initialize ./neo4j/data again."
create_neo4j_backup neo4j-4416 1
mkdir -p ./neo4j/data

pause_and_prompt "Step ${step}. We start a 5.3.0 container in bash mode"
let step++
start_neo4j_bash neo4j-530-bash ${neo4j_530}

pause_and_prompt "Step ${step}. Now we import and migrate (forcing all BTREE indices to RANGE)."
let step++
execute_container_command neo4j-530-bash '/var/lib/neo4j/bin/neo4j-admin database load --overwrite-destination=true --from-path=/imports neo4j'
execute_container_command neo4j-530-bash '/var/lib/neo4j/bin/neo4j-admin database migrate neo4j --force-btree-indexes-to-range'

pause_and_prompt "Step ${step}. Shut down 5.3.0 container in bash mode."
let step++
stop_and_remove_container neo4j-530-bash

pause_and_prompt "We start 5.3.0 container normally. Connect to localhost:7474 to check the database and index state."
start_neo4j neo4j ${neo4j_530}
timeout 30s docker logs -f neo4j-4416

echo Done
