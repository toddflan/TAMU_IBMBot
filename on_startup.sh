#!/bin/bash

# Make bluetooth discoverable
sleep 5
sudo hciconfig hci0 up
sudo hciconfig hci0 piscan
sleep 5

# Run python script for bluetooth SECRET HANDSHAKE with app
sudo python /home/pi/Desktop/TAMU_IBMBot/UserData/bt_secret_handshake/internet.py

# Wait for wifi connection
sleep 10

# Speak intro
curl -X POST -d "Thanks for connecting me to the internet! I'm your IBM Senior Assistant, but you can call me TJ." -H "Content-type: text/plain" http://localhost:1880/reminder

# Wait for intro to finish
sleep 20
