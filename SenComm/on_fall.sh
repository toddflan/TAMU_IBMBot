#!/bin/bash

# Upon filechange, generate message and add command to cron daemon

file="falls.txt"

while true
do
	inotifywait -e modify $file
	curl -X POST -d "I've detected a fall. Would you like me to get help?" -H "Content-type: text/plain" http://localhost:1880/reminder
done
