#!/bin/bash

# Migration script for Neo4j 5.3.0/5.12.0 to 5.26.19 LTS
#
# This script migrates Neo4j within the 5.x family, which is much simpler
# than the 4.x to 5.x migration since:
# - Store format is compatible within 5.x (automatic upgrade)
# - No intermediate version needed
# - No index migration required
# - Same neo4j-admin command syntax

#
# Definitions
#

# Parse options
OPTS=`getopt -o iuh -n migrate.sh -- "$@"`

INTERACTIVE=0
UNDO=0

while true; do
  case "$1" in
    -i ) INTERACTIVE=1; shift 1;;
    -u ) UNDO=1; echo "Attempt to undo and restore previous version"; shift 1;;
    -h ) echo -e "This script migrates Neo4j graph database from 5.3.0/5.12.0 to 5.26.19 LTS.\n Use -i to force prompted interactive mode.\n Use -u to try to put things back as they were."; exit 0;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

# Container definitions
neo4j_old="fabrictestbed/neo4j-apoc:5.3.0"  # or 5.12.0
neo4j_new="fabrictestbed/neo4j-apoc:5.26.19"

neo4j_old_name="neo4j-old"
neo4j_new_name="neo4j"

# Container start command
container_start_prefix="docker run -d --user=$(id -u):$(id -g) --publish=7473:7473 --publish=7474:7474 --publish=7687:7687 --volume=$(pwd)/neo4j/data:/data --volume=$(pwd)/neo4j/imports:/imports -e NEO4J_AUTH=neo4j/password"

# Backup files
backup_tar="neo4j-5x-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
backup_marker=".neo4j-5x-backup-latest"

#
# Helper functions
#

function pause_and_prompt {
  if [ ${INTERACTIVE} -eq 1 ]; then
    echo -e "\n*** ${1}"
    read -p "Press ENTER to continue or Ctrl-C to stop" _
  else
    echo -e "\n*** ${1}"
  fi
}

function error_msg {
  echo -e "\nERROR: ${1}"
  exit 1
}

function stop_and_remove_container {
  local _cont_name=$1
  echo "Stopping and removing container ${_cont_name} if it exists"
  docker container stop ${_cont_name} 2>/dev/null
  docker container rm ${_cont_name} 2>/dev/null
}

function create_neo4j_backup {
  local _backup_file=$1
  echo "Creating backup: ${_backup_file}"
  tar -czf ${_backup_file} neo4j/
  if [ $? -eq 0 ]; then
    echo ${_backup_file} > ${backup_marker}
    echo "Backup created successfully: ${_backup_file}"
  else
    error_msg "Failed to create backup"
  fi
}

function restore_neo4j_backup {
  if [ ! -f ${backup_marker} ]; then
    error_msg "No backup marker found. Cannot determine which backup to restore."
  fi
  local _backup_file=$(cat ${backup_marker})
  if [ ! -f ${_backup_file} ]; then
    error_msg "Backup file ${_backup_file} not found"
  fi
  echo "Restoring from backup: ${_backup_file}"
  rm -rf neo4j/
  tar -xzf ${_backup_file}
  if [ $? -eq 0 ]; then
    echo "Backup restored successfully"
  else
    error_msg "Failed to restore backup"
  fi
}

#
# Main sequence
#

if [ $UNDO -eq 1 ]; then
  echo "UNDO mode: Restoring from backup"
  stop_and_remove_container ${neo4j_new_name}
  restore_neo4j_backup
  echo "Restore complete. You can now start your previous Neo4j version."
  exit 0
fi

let step=1

# Verify we're in the right location
pause_and_prompt "Step ${step}. Verify neo4j/ directory exists"
if [ ! -d ./neo4j ]; then
  error_msg "Must run from above neo4j/ directory"
fi
echo "Found neo4j/ directory"
let step++

# Stop any running containers
pause_and_prompt "Step ${step}. Stop any running Neo4j containers"
stop_and_remove_container neo4j
stop_and_remove_container ${neo4j_old_name}
stop_and_remove_container ${neo4j_new_name}
let step++

# Create backup
pause_and_prompt "Step ${step}. Create backup of current database"
create_neo4j_backup ${backup_tar}
let step++

# Optional: Create dump for portability
pause_and_prompt "Step ${step}. (Optional) Create database dump for maximum safety"
echo "Starting temporary container to create dump..."
docker run -d --user=$(id -u):$(id -g) --name=neo4j-dump \
  --volume=$(pwd)/neo4j/data:/data \
  --volume=$(pwd)/neo4j/imports:/imports \
  -e NEO4J_AUTH=neo4j/password \
  ${neo4j_old} sleep infinity

if [ $? -eq 0 ]; then
  echo "Creating dump file (this may take several minutes)..."
  docker exec neo4j-dump neo4j-admin database dump neo4j --to-path=/imports 2>&1 | grep -v "WARNING"
  if [ $? -eq 0 ]; then
    echo "Dump created successfully in neo4j/imports/"
  else
    echo "Warning: Dump creation failed or was skipped"
  fi
  stop_and_remove_container neo4j-dump
else
  echo "Warning: Could not create dump container, skipping dump step"
fi
let step++

# Start new version
pause_and_prompt "Step ${step}. Start Neo4j 5.26.19 container (automatic upgrade occurs)"
echo "Starting Neo4j 5.26.19..."
${container_start_prefix} --name=${neo4j_new_name} ${neo4j_new}

if [ $? -ne 0 ]; then
  error_msg "Failed to start Neo4j 5.26.19 container"
fi

echo "Container started. Waiting for Neo4j to initialize..."
sleep 5
let step++

# Monitor upgrade
pause_and_prompt "Step ${step}. Monitor logs for successful startup"
echo "Monitoring logs for 30 seconds (Ctrl-C to stop monitoring, migration continues)..."
timeout 30s docker logs -f ${neo4j_new_name} 2>&1 || true
let step++

# Verify
echo ""
echo "=========================================="
echo "Migration steps complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Verify Neo4j is running: docker logs ${neo4j_new_name}"
echo "2. Open web UI at http://localhost:7474"
echo "3. Login with neo4j/password"
echo "4. Check version with: CALL dbms.components()"
echo "5. Verify your data is intact"
echo ""
echo "If issues occur, use -u option to restore from backup:"
echo "  $0 -u"
echo ""
echo "Backup saved at: ${backup_tar}"
echo "=========================================="
