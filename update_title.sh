#!/bin/bash

powershell.exe -Command "& {.\\venv\\bin\\Activate.ps1}"
powershell.exe -Command "& {python.exe update_youtube_title.py update}"

