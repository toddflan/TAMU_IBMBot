#!/bin/bash
# Script to remind user.

#echo -e "Enter med filename: "
#read filename

# Generates reminder message, triggers bot to say it
# Runs in correct directory, needed because cron runs in $home

$(cd /home/pi/Desktop/TAMU_IBMBot/UserData/; ./msg med1.txt msg_out.txt; curl -X POST -d @msg_out.txt -H "Content-type: text/plain" http://localhost:1880/reminder)
