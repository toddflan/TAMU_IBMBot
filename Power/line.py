from __future__ import print_function
from __future__ import division


# import the GoPiGo3 drivers
import time, cmd, sys
import easygopigo3 as easy
import line_sensor


# This example is a simple following scheme

# Create an instance of the GoPiGo3 class.
# GPG will be the GoPiGo3 object.
gpg = easy.EasyGoPiGo3()

#Calibrate speed at first run
#100 is good with fresh batteries
#125 for batteries with half capacityfwd_speed=110                                              # Forward speed at which the GoPiGo should run.

fwd_speed=100                                                                        # If you're swinging too hard around your line
                                                                        # reduce this speed.
poll_time=0.01                                          # Time between polling the sensor, seconds.

slight_turn_speed=int(.7*fwd_speed)
turn_speed=int(.7*fwd_speed)

last_val=[0]*5                                          # An array to keep track of the previous values.
curr=[0]*5                                                      # An array to keep track of the current values.

gpg.set_speed(fwd_speed)

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
        if curr==small_r or curr==small_l or curr==mid or curr==mid1:
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

startup = 1

for trash in range(5):   # throw away bad data
	curr = absolute_line_pos()

while True:
        last_val=curr
        curr=absolute_line_pos()
        print(curr)

        if startup == 1:
                print ("in startup")
                if curr == stop1:
                        go_straight()
                else: #curr == stop:
                        go_straight()
                        time.sleep(0.5)
                        gpg.turn_degrees(90)
                        time.sleep(1)
                        startup = 0
                #else:
                        #go_straight()#startup = 0
                time.sleep(poll_time)

        #if startup == 1:
                #if curr == stop1:
                        #go_straight()
                #elif curr == left or curr == left1:
                        #turn_left()
                #elif curr == right or curr == right1:
                        #turn_right()
                #elif curr == mid and corr == mid1:
                        #run_gpg(curr)
                        #startup = 0
        #white line reached
        #if curr== stop1:
                #go_straight()
                #if msg_en:
                        #print("White found, last cmd running")
                #for i in range(5):
                        #run_gpg(last_val)
        else:
                #if curr == stop:
                        #gpg.stop()
                #else:
                        run_gpg(curr)
