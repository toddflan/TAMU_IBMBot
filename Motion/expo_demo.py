
# import the GoPiGo3 drivers
import time, cmd, sys
import easygopigo3 as easy
import serial

#This sets up the serial input
ser = serial.Serial(
    '/dev/ttyAMA0' ,\
    baudrate = 115200)

# This example is a simple following scheme

# Create an instance of the GoPiGo3 class.
# GPG will be the GoPiGo3 object.
gpg = easy.EasyGoPiGo3()

# Create an instance of the Distance Sensor class.
distance = gpg.init_distance_sensor()
dist = 0
garbage = 0
data = 0
old = 50

# Open a file
#f = open('data', 'w')
#f.truncate()

try:
        gpg.set_speed(400)
        while True:
                for d in ser.read():
                        data = d
                X = int(data)
                #print("X: ",X)
                if(~garbage):
                        if (X < 0 or X > 82):
                                print("Out of range?")
                                gpg.stop()
                                garbage = 0
                        elif(X == 81):
                                gpg.turn_degrees(45)
                        elif(X < 30):
                                #print("Turn Left!")
                                gpg.stop()
                                degrees = (X-40)*(0.5*25/40)
                                #print("D: ", degrees)
                                gpg.turn_degrees(degrees)
                                garbage = 1
                        elif(X > 50):
                                #print("Turn Right!")
                                gpg.stop()
                                degrees = (X-40)*(0.5*50/40)
                                #print("D: ", degrees)
                                gpg.turn_degrees(degrees)
                                garbage = 1
                        print ("X : ", X)
                else:
                        garbage = 0

        GPG.reset_all()

except KeyboardInterrupt:       # except the program gets interrupted by Ctrl+C on the keyboard.
        gpg.reset_all()         # Unconfigure the sensors, disable the motors, and restore the LED to the control of the GoPiGo3 firmware.
