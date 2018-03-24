#!/bin/bash

# Make bluetooth discoverable
sudo hciconfig hci0 piscan

# Run python script for bluetooth SECRET HANDSHAKE with app
sudo python internet.py

# Wait for wifi connection
sleep 10

# Speak intro
#curl -X POST -d "Thanks for connecting me to the internet! I'm your IBM Senior Assistant, but you can call me TJ." -H "Content-type: text/plain" http://localhost:1880/reminder

# Wait for intro to finish
#sleep 20
