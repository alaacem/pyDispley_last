#!/bin/bash

# Declare an associative array with processes and their descriptors
declare -A processes=(
    ["main.py"]="main"
    ["anzeige_flask.py"]="anzeige_flask"
    ["key.py"]="key"
    ["chromium-browser"]="browser"
    ["scrapping.py"]="scrapping"
)

# Function to kill processes
kill_process() {
    local process=$1
    local descriptor=$2

    if pgrep -f "$process" > /dev/null; then
        sudo pkill -f "$process"
        echo "Killed the $descriptor process."
    else
        echo "No $descriptor process was found running."
    fi
}

# Main logic
for process in "${!processes[@]}"; do
    kill_process "$process" "${processes[$process]}"
done
