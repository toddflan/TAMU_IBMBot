#!/bin/bash

# Script to remind user.

# Triggers bot to say reminder message
# Runs in correct directory, needed because cron runs in $home

$(cd /home/pi/Desktop/TAMU_IBMBot/UserData/test/; curl -X POST -d @med0_out.txt -H "Content-type: text/plain" http://localhost:1880/reminder)
