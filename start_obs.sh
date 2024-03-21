#!/bin/bash

# Check if OBS Studio is running
if tasklist.exe | grep -q "obs64.exe"
then
    echo "OBS Studio is already running."
else
    echo "Starting OBS Studio."
    cd /
    cd /mnt/c/
    cd 'Program Files'
    cd obs-studio/bin/64bit
    ./obs64.exe &
fi

echo Started OBS successfully