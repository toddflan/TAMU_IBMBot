#!/bin/bash
# Script to remind user.

# Get filename

echo -e "Enter med filename: "
read filename

# Generate reminder, trigger bot to say it

./msg $filename msg_out.txt
curl -X POST -d @msg_out.txt -H "Content-type: text/plain" http://localhost:1880/reminder
