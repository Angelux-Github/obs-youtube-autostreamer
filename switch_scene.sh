#!/bin/bash

#obs.py swicth scenes

source venv/bin/activate
python3 obs.py switch_scene $1
deactivate
