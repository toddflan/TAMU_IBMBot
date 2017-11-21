#!/bin/bash

# Add reminder commands to cron daemon

medfile="med0.txt"
dir="/home/pi/Desktop/TAMU_IBMBot/UserData/test/remind.sh"

(crontab -l; ./read Minute $medfile; printf " "; ./read Hour $medfile; printf " * * "; ./read Day $medfile; echo " bash $dir") | crontab -
