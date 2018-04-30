from __future__ import print_function
from __future__ import division

# import the GoPiGo3 drivers
import time, cmd, sys
import easygopigo3 as easy
import serial
import line_sensor

#This sets up the serial input
ser = serial.Serial(
    '/dev/ttyAMA0' ,\
    baudrate = 115200)

# This example is a simple following scheme

# Create an instance of the GoPiGo3 class.
# GPG will be the GoPiGo3 object.
gpg = easy.EasyGoPiGo3()

# line following functions
fwd_speed = 100
poll_time = 0.01

slight_turn_speed=int(.7*fwd_speed)
turn_speed=int(.7*fwd_speed)

last_val=[0]*5                                          # An array to keep track of the previous values.
curr=[0]*5                                                      # An array to keep track of the current values.


gpg_en=1                                                        #Enable/disable gopigo
msg_en=1                                                        #Enable messages on screen.  Turn this off if you don't want messages.

#Get line parameters
line_pos=[0]*5
white_line=line_sensor.get_white_line()
black_line=line_sensor.get_black_line()
range_sensor= line_sensor.get_range()
threshold=[a+b/2 for a,b in zip(white_line,range_sensor)]       # Make an iterator that aggregates elements from each of the iterables.

#Position to take action on
mid     =[0,0,1,0,0]    # Middle Position.
mid1    =[0,1,1,1,0]    # Middle Position.
small_l =[0,1,1,0,0]    # Slightly to the left.
small_l1=[0,1,0,0,0]    # Slightly to the left.
small_r =[0,0,1,1,0]    # Slightly to the right.
small_r1=[0,0,0,1,0]    # Slightly to the right.
left    =[1,1,0,1,0]    # Strong left.
left1   =[1,0,0,1,0]    # Strong left.
right   =[0,0,0,1,1]    # Sensor reads strongly to the right.
right1  =[0,0,0,0,1]    # Sensor reads strongly to the right.
stop    =[1,1,1,1,1]    # Sensor reads stop.
stop1   =[0,0,0,1,0]    # Sensor reads stop.
dumb    =[0,1,0,1,0]    # Stupid bad sensor

thresh = 800

#Converts the raw values to absolute 0 and 1 depending on the threshold set
def absolute_line_pos():
        raw_vals=line_sensor.get_sensorval()
        for i in range(5):
                if raw_vals[i]>thresh:#threshold[i]:
                        line_pos[i]=1
                else:
                        line_pos[i]=0
        return line_pos

#GoPiGo actions
def go_straight():
        if msg_en:
                print("Going straight")
        if gpg_en:
                gpg.set_speed(fwd_speed)
                gpg.forward()

def turn_slight_left():
        if msg_en:
                print("Turn slight left")
        if gpg_en:
                #gpg.set_right_speed(slight_turn_speed)
                gpg.turn_degrees(-15) #gpg.set_left_speed(fwd_speed)
                #gpg.forward()

def turn_left():
        if msg_en:
                print("Turn left")
        if gpg_en:
                #gpg.set_speed(turn_speed)
                gpg.turn_degrees(-30) #gpg.left()

def turn_slight_right():
        if msg_en:
                print("Turn slight right")
        if gpg_en:
                #gpg.set_right_speed(fwd_speed)
                gpg.turn_degrees(15) #gpg.set_left_speed(slight_turn_speed)
                #gpg.forward()

def turn_right():
        if msg_en:
                print("Turn right")
        if gpg_en:
                #gpg.set_speed(turn_speed)
                gpg.turn_degrees(30) #gpg.right()

def stop_now():
        if msg_en:
                print("Stop")
        if gpg_en:
                gpg.stop()

def go_back():
        if msg_en:
                print("Go Back")
        if gpg_en:
                gpg.set_speed(turn_speed)
                gpg.backward()

#Action to run when a line is detected
def run_gpg(curr):
        #if the line is in the middle, keep moving straight
        #if the line is slightly left of right, keep moving straight
        if curr==small_r or curr==small_l or curr==mid or curr==mid1 or curr==dumb:
                go_straight()

        #If the line is towards the sligh left, turn slight right
        #elif curr==small_l1:
                #turn_slight_right()
        elif curr==left or curr==left1:
                turn_right()

        #If the line is towards the sligh right, turn slight left
        #elif curr==small_r1:
                #turn_slight_left()
        elif curr==right or curr==right1:
                turn_left()
        elif curr==stop:
                gpg.stop()
#                gpg.turn_degrees(90)
                #go_straight()
                #time.sleep(0.5)
                #gpg.turn_degrees(90)
#                #go_straight()
                #time.sleep(0.5)
        time.sleep(poll_time)



# Create an instance of the Distance Sensor class.
distance = gpg.init_distance_sensor()
dist = 0
garbage = 0
data = 0
old = 50

# Open a file
#f = open('data', 'w')
#f.truncate()

line_follow = 0
startup = 1

gpg.set_speed(450)

try:
        #gpg.set_speed(450)
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
                        else:
                                new = distance.read_inches()
                                if((new-old) <= 50):
                                        dist = new
                                garbage = 0
                                #print("D: ",D)
                                if(dist > 45):
                                        gpg.forward()
                                #elif(dist < ):
                                        #gpg.backward()
                                elif(dist != 0):
                                        gpg.stop()
                                        line_follow = 1
                                        
                                old = new
                        print("X: ", X, "     D: ", dist)
                else:
                        garbage = 0

                # line following
                gpg.set_speed(fwd_speed)

                for trash in range(5):   # throw away bad data
	                curr = absolute_line_pos()

                while line_follow == 1:
                        last_val=curr
                        curr=absolute_line_pos()
                        print(curr)

                        if startup == 1:
                                print ("in startup")
                                if curr == stop1:
                                        go_straight()
                                else:
                                        go_straight()
                                        time.sleep(0.5)
                                        gpg.turn_degrees(90)
                                        time.sleep(1)
                                        startup = 0
                                time.sleep(poll_time)
                        else:
                                run_gpg(curr)

        gpg.reset_all()

except KeyboardInterrupt:       # except the program gets interrupted by Ctrl+C on the keyboard.
        gpg.reset_all()         # Unconfigure the sensors, disable the motors, and restore the LED to the control of the GoPiGo3 firmware.
