import sys
import os
import json
import subprocess

print("#### STARTING PYTHON SCRIPT ####")

# Read values from the JSON file
try:
    with open('../user_data/websocket_config.json', 'r') as json_file:
        config = json.load(json_file)
except FileNotFoundError:
    print("The json file or directory does not exist. Please check the path and try again.")
    print("You must create the websocket_config.json file to establish a connection to OBS")
    print("Aborting process - obs_functions.py Module - ip_address, port, password")
    sys.exit(1)

# Set OBS WebSocket server Address and Port
obs_host = config['ip_address']
obs_port = config['port']
obs_password = config['password']

def execute_obs_command(command):
    full_command = f'obs-cmd.exe --websocket obsws://{obs_host}:{obs_port}/{obs_password} {command}'
    try:
        subprocess.run(full_command, check=True, shell=True, text=True)
        print(f"Executed command: {full_command}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")





def switch_scene(scene_name):
    execute_obs_command(f'scene current "{scene_name}"')


def start_recording():
    execute_obs_command("recording start")

def stop_recording():
    execute_obs_command("recording stop")

def start_streaming():
    execute_obs_command("streaming start")

def stop_streaming():
    execute_obs_command("streaming stop")



def start_obs():
    obs_dir = r"C:\Program Files\obs-studio\bin\64bit"
    obs_path = os.path.join(obs_dir, "obs64.exe")
    # Check if OBS is already running
    if "obs64.exe" in os.popen('tasklist').read():
        print("OBS Studio is already running.")
    else:
        print("Starting OBS Studio.")
        try:
            os.chdir(obs_dir)  # Change to OBS directory
            os.startfile(obs_path)
            print("Started OBS successfully")
        except Exception as e:
            print(f"Error starting OBS: {e}")



# Main code
if len(sys.argv) > 1:
    function_name = sys.argv[1]

    if function_name == "switch_scene" and len(sys.argv) > 2:
        scene_name = sys.argv[2]
        switch_scene(scene_name)
    elif function_name == "start_recording":
        start_recording()
    elif function_name == "stop_recording":
        stop_recording()
    elif function_name == "start_streaming":
        start_streaming()
    elif function_name == "stop_streaming":
        stop_streaming()
    elif function_name == "start_obs":
        start_obs()
