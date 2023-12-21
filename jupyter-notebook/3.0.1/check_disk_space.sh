#!/bin/bash

# Function to check disk space and display a message if usage exceeds the threshold
check_disk_space() {
    local threshold="$1"
    local disk_usage=$(df -h /home/fabric/work/ | awk 'NR==2 {print $5}' | tr -d '%')
    if [ "$disk_usage" -gt "$threshold" ]; then
        echo -e "\n\033[1;31mWarning: Disk space usage is greater than $threshold% ($disk_usage%). Consider freeing up space by removing old jupyter-examples-* directories.\033[0m\n"
    fi
}

# Check if a threshold value is provided as a command-line argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <threshold>"
    exit 1
fi

# Extract the threshold value from the command-line argument
threshold="$1"

# Call the disk space check function with the provided threshold
check_disk_space "$threshold"

