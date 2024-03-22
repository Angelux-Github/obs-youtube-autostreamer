# PowerShell Script: run_title_get_input.ps1

# Activate the virtual environment
. "C:\Users\angel\userScripts\obsStream\venv\bin\Activate.ps1"

# Run the Python script with the 'stream_file_input' argument
python.exe "C:\Users\angel\userScripts\obsStream\update_youtube_title.py" stream_file_input
