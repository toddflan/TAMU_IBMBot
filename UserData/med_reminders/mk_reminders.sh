#!/bin/bash

# Generate reminder message files

# will need to do while loop for all meds******************

# Check if files exist and have data
if [ -s meds/med1.txt ]
then
	./mk_remind_msg meds/med1.txt med1_out.txt
fi

if [ -s meds/med2.txt ]
then
	./mk_remind_msg meds/med2.txt med2_out.txt
fi

if [ -s meds/med3.txt ]
then
	./mk_remind_msg meds/med3.txt med3_out.txt
fi
