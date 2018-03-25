
# import the GoPiGo3 drivers
import time, cmd, sys
import easygopigo3 as easy

# This example is a simple following scheme

# Create an instance of the GoPiGo3 class.
# GPG will be the GoPiGo3 object.
gpg = easy.EasyGoPiGo3()

# Create an instance of the Distance Sensor class.
distance = gpg.init_distance_sensor()
dist = 0

# Open a file
#f = open('data', 'w')
#f.truncate()

##try:
##    while True:
##        # Directly print the values of the sensor.
##        print(str(distance.read_inches()))
##        dist = distance.read_inches()
##        f.write(str(dist)+'\n')
##        if(dist > 40):
##            gpg.forward()
##        elif(dist < 32):
##            gpg.backward()
##        else:
##            gpg.stop()
##        time.sleep(.25)

try:
        gpg.set_speed(100)
        while True:
                try:
			#input a pixel location
                        X=int(input("Input an X value between 0 and 79 inclusive:"))
                except ValueError:
                        print("Not a number")
                if (X < 0 or X > 79):
                        print("Out of range")
                elif(X < 30):
			#if the number is oustide the middle 20 pixels, turn
                        #degrees = (X-40)*.75
                        #print("Degrees: " + str(degrees))
                        gpg.left()
                elif(X > 50):
                        gpg.right()
                else:
##			#if the number is inside the threshold, use the distance sensor
##                        dist = distance.read_inches()
##                        while(dist > 40 or dist < 32):
##                                if(dist > 40):
##                                        gpg.forward()
##                                elif(dist < 32):
##                                        gpg.backward()
##                                else:
##                                        gpg.stop()
##                                dist = distance.read_inches()
##                                print("Distance: " + str(dist))
                        gpg.stop()
        gpg.reset_all()

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        gpg.reset_all()       # Unconfigure the sensors, disable the motors, and restore the LED to the control of the GoPiGo3 firmware.

	

