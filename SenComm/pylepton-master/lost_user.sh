#!/bin/bash

# Alert user that we've lost them
curl -X POST -d "Hello. I seem to have lost you. Please come back." -H "Content-type: text/plain" http://localhost:1880/reminder
