#!/bin/bash

# Script to remind user.

dir="/home/pi/Desktop/TAMU_IBMBot/UserData/med_reminders/"

# Triggers bot to say reminder message
# Runs in correct directory, needed because cron runs in $home

cd $dir; curl -X POST -d @med3_out.txt -H "Content-type: text/plain" http://tjSA:1880/reminder
