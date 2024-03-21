import sys
import obswebsocket
from obswebsocket import obsws, requests
import json

print("#### STARTING PYTHON SCRIPT ####")
# Read values from the JSON file
with open('websocket_config.json', 'r') as json_file:
    config = json.load(json_file)

# Set OBS WebSocket server Address and Port
obs_host = config['ip_address']
obs_port = config['port']
obs_password = config['password']



# Connect to OBS using obs-websocket-py
obs = obsws(obs_host, obs_port, obs_password)
try:
    obs.connect()
    print("Connected to OBS WebSocket server")
except Exception as e:
    print(f"Failed to connect to OBS: {e}")
    sys.exit(1)


def switch_scene(scene_name):
    try:
        obs.call(requests.SetCurrentProgramScene(sceneName=scene_name))
        print(f"Switched to scene: {scene_name}")
    except Exception as e:
        print(f"Error switching scene: {e}")


# Main code
if len(sys.argv) > 1:
    function_name = sys.argv[1]

    if function_name == "switch_scene" and len(sys.argv) > 2:
        scene_name = sys.argv[2]
        switch_scene(scene_name)

obs.disconnect()
print("Disconnected from OBS WebSocket server")
print("#### ENDING PYTHON SCRIPT ####")
