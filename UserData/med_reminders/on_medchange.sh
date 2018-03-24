#!/bin/bash

# Upon filechange, generate message and add command to cron daemon

file="meds/"

while true
do
	inotifywait -e modify $file
	bash mk_reminders.sh
	bash add_2_cron.sh
done
