#!/bin/bash
# Add reminder programs to cron daemon

(crontab -l; ./read_new Minute med0.txt; printf " "; ./read_new Hour med0.txt; echo " * * * bash /home/pi/Desktop/TAMU_IBMBot/UserData/remind0.sh") | crontab -
