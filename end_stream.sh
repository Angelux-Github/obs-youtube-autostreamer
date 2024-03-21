#!/bin/bash


# Read values from the JSON file
ip_address=$(jq -r '.ip_address' websocket_config.json)
port=$(jq -r '.port' websocket_config.json)
password=$(jq -r '.password' websocket_config.json)

# Print the values
echo "IP Address: $ip_address"
echo "Port: $port"
echo "Password: $password"

#command to start values (Modify Values to Your own (IP ADDRESS, PORT, PASSORD)):
obs-cmd.exe --websocket obsws://$ip_address:$port/$password streaming stop