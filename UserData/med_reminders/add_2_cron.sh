#!/bin/bash

# Add reminder commands to cron daemon

medfile1="meds/med1.txt"
medfile2="meds/med2.txt"
medfile3="meds/med3.txt"
dir1="/home/pi/Desktop/TAMU_IBMBot/UserData/test/remind1.sh"
dir2="/home/pi/Desktop/TAMU_IBMBot/UserData/test/remind2.sh"
dir3="/home/pi/Desktop/TAMU_IBMBot/UserData/test/remind3.sh"

# Replace commands in crontab if new command is available
if [ -s $medfile1 ]
then
	crontab -u pi -l | grep -v $dir1 | crontab -u pi -
	(crontab -l; ./read Minute $medfile1; printf " "; ./read Hour $medfile1; printf " * * "; ./read Day $medfile1; echo " bash $dir1") | crontab -
fi

if [ -s $medfile2 ]
then
	crontab -u pi -l | grep -v $dir2 | crontab -u pi -
	(crontab -l; ./read Minute $medfile2; printf " "; ./read Hour $medfile2; printf " * * "; ./read Day $medfile2; echo " bash $dir2") | crontab -
fi

if [ -s $medfile3 ]
then
	crontab -u pi -l | grep -v $dir3 | crontab -u pi -
	(crontab -l; ./read Minute $medfile3; printf " "; ./read Hour $medfile3; printf " * * "; ./read Day $medfile3; echo " bash $dir3") | crontab -
fi
