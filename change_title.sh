#!/bin/bash

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "No title provided. Usage: ./change_title.sh 'New Title'"
    exit 1
fi

# Write the provided argument to the stream_title.txt file
echo "$1" > stream_title.txt
echo "Title updated to: $1"

powershell.exe -Command "& {.\\venv\\bin\\Activate.ps1}"
powershell.exe -Command "& {python.exe update_youtube_title.py update}"