#!/bin/bash

# Directories
med_dir="/home/pi/Desktop/TAMU_IBMBot/UserData/med_reminders/"
accel_dir="/home/pi/Desktop/TAMU_IBMBot/SenComm/"
ir_dir="/home/pi/Desktop/TAMU_IBMBot/SenComm/pylepton-master/"

# Make bluetooth discoverable
sleep 5
sudo hciconfig hci0 up
sudo hciconfig hci0 piscan
sleep 5

# Run python script for bluetooth SECRET HANDSHAKE with app, save IP address
ip_addr=$(sudo python /home/pi/Desktop/TAMU_IBMBot/UserData/bt_secret_handshake/internet.py | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b")

# grep for ip address command found online @ stackexchange "How to tell if any IP address is present..."

# Wait for wifi connection
sleep 10

# Speak intro
curl -X POST -d "Thanks for connecting me to the internet! I'm your IBM Senior Assistant, but you can call me TJ." -H "Content-type: text/plain" http://localhost:1880/reminder

# Wait for intro to finish
sleep 10

# MEDICATION REMINDERS ***************************
curl -X POST -d "Starting medication reminder server." -H "Content-type: text/plain" http://localhost:1880/reminder

# Get to med directory
cd $med_dir

# Start med data watchers
bash on_medchange.sh &

# Start med data server
./server $ip_addr 5000 &

# Wait
sleep 5

# FALL DETECTION ***********************************
curl -X POST -d "Starting fall detection." -H "Content-type: text/plain" http://localhost:1880/reminder

# Get to accelerometer code
cd $accel_dir

# Initialize BT for the accelerometer
bash BT.sh

# Start fall detection
python fall_detection.py &

# Wait
sleep 5

# FOLLOWING A USER ****************************
curl -X POST -d "Starting following code." -H "Content-type: text/plain" http://localhost:1880/reminder

# Switch user to pi (not root) and start following code
sudo -u pi -H bash -c "cd $ir_dir; source /home/pi/.profile; workon cv3; python IR_test_contour.py"
