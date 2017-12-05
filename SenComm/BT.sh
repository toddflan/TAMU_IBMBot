#!/bin/bash

# Bind bluetooth accelerometer to rfcomm0
sudo modprobe rfcomm
sudo rfcomm bind rfcomm0 20:17:03:22:25:05

# Check if it worked
ls /dev | grep rfcomm
