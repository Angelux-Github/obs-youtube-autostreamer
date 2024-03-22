#!/bin/bash

# Get the current working directory in WSL
current_dir=$(pwd)

# Convert the WSL path to a Windows path
windows_path=$(wslpath -w "$current_dir")

# Define the path to your Python script
python_script_name="update_youtube_title.py"
python_script_path="$windows_path\\$python_script_name"

# Define the path to your virtual environment's activate script
venv_activate_path="$windows_path\\venv\\bin\\Activate.ps1"

# Create the PowerShell script
cat > run_title_get_input.ps1 <<EOF
# PowerShell Script: run_title_get_input.ps1

# Activate the virtual environment
. "$venv_activate_path"

# Run the Python script with the 'stream_file_input' argument
python.exe "$python_script_path" stream_file_input
EOF

# Run the newly created PowerShell script
powershell.exe -Command "& {.\run_title_get_input.ps1}"

