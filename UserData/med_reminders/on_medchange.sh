#!/bin/bash

# Upon filechange, generate message and add command to cron daemon

file="/home/pi/Desktop/TAMU_IBMBot/UserData/med_reminders/meds/"

while true
do
	inotifywait -e modify $file
	bash /home/pi/Desktop/TAMU_IBMBot/UserData/med_reminders/mk_reminders.sh
	bash /home/pi/Desktop/TAMU_IBMBot/UserData/med_reminders/add_2_cron.sh
done
