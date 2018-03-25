#!/usr/bin/env python
#
# https://www.dexterindustries.com/GoPiGo/
# https://github.com/DexterInd/GoPiGo3
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md
#
# This code is an example for making the GoPiGo3 turn accurately
#
# Results:  When you run this program, the GoPiGo3 should turn 90 degrees to the right, 180 to the left, and then 90 to the right, ending where it started.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time    # import the time library for the sleep function
import gopigo3 # import the GoPiGo3 drivers
import cmd,sys     # import command line input functions

GPG = gopigo3.GoPiGo3() # Create an instance of the GoPiGo3 class. GPG will be the GoPiGo3 object.

def TurnDegrees(degrees, speed):
    # get the starting position of each motor
    StartPositionLeft      = GPG.get_motor_encoder(GPG.MOTOR_LEFT)
    StartPositionRight     = GPG.get_motor_encoder(GPG.MOTOR_RIGHT)
    print("SLeft: ", StartPositionLeft,"Right: ", StartPositionRight) 
    
    # the distance in mm that each wheel needs to travel
    WheelTravelDistance    = ((GPG.WHEEL_BASE_CIRCUMFERENCE * degrees) / 360)
    
    # the number of degrees each wheel needs to turn
    WheelTurnDegrees       = ((WheelTravelDistance / GPG.WHEEL_CIRCUMFERENCE) * 360)
    print("WTD: ",WheelTurnDegrees)

    # Limit the speed
    GPG.set_motor_limits(GPG.MOTOR_LEFT + GPG.MOTOR_RIGHT, dps = speed)
    
    # Set each motor target
    GPG.set_motor_position(GPG.MOTOR_LEFT, (StartPositionLeft + WheelTurnDegrees))
    GPG.set_motor_position(GPG.MOTOR_RIGHT, (StartPositionRight - WheelTurnDegrees))

try:
    while True:
        try:
           X=int(input('Input an X value between 0 and 79 inclusive:'))
        except ValueError:
           print("Not a number")
        if (X < 0 or X > 79):
           print("Out of range")
        elif(X < 30 or X > 50):
           degrees = (X-40)/40*30
           print("Degrees: " + str(degrees))
           TurnDegrees(degrees, 100)
        else:
           GPG.forward()
           time.sleep(.25)
           GPG.stop()
    GPG.reset_all()

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    GPG.reset_all()        # Unconfigure the sensors, disable and reset the motors, and turn off LEDs
