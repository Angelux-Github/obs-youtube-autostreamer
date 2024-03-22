#!/bin/bash
sudo apt install jq
obsDirectory=$(pwd)
winObsDirectory=$(wslpath -w "$obsDirectory")

powershell.exe -Command "& {'$winObsDirectory\\venv\\bin\\Activate.ps1'; pip install -r req_windows_powershell_python.txt}"





