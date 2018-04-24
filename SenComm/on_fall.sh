#!/bin/bash

# Message to user
curl -X POST -d "I've detected a fall. Would you like me to get help?" -H "Content-type: text/plain" http://tjSA:1880/reminder

# Start conversation
curl -X POST -d "start" -H "Content-type: text/plain" http://localhost:1880/fallconf &

# Wait
sleep 10

# Stop conversation
curl -X POST -d "stop" -H "Content-type: text/plain" http://localhost:1880/fallconf &
