import serial
import math
import subprocess			# to call bash scripts

# Function for decoding accelerometer data
def getAccel(num):
	if (num & 0x8000) == 0x8000:	# if MSB is 1 (negative number)
		return (num - 65536) / 32768.0 * 16	# convert twos complement to negative integer
	else:
		return num / 32768.0 * 16

# Serial connection
ser = serial.Serial('/dev/rfcomm0', 115200)

iter = 0
threshold = 2.0		# Fall detection
above_count = 0

has_fallen = 0		# need to trigger get help text

fall_msg_sent = 0	# to not overload node red with messages

# Get data
while 1:
	result = ord(ser.read())
	if result == 0x55:		# Code before data
		data = []
		data.append(result)
		for i in range(1,10):
			data.append(ord(ser.read()))
		if data[1] == 0x51:	# Code before acceleration data
			a_x = (data[3] << 8 | data[2])		# 16 bit twos complement integers
			a_y = (data[5] << 8 | data[4])
			a_z = (data[7] << 8 | data[6])

			a_x = getAccel(a_x)
			a_y = getAccel(a_y)
			a_z = getAccel(a_z)

			vect_mag = math.sqrt(a_x**2 + a_y**2 + a_z**2)

			if vect_mag > threshold:	# Detect fall
				above_count = above_count + 1
			else:
				above_count = 0

			if above_count > 2:		# Gets rid of bad spikes
				if fall_msg_sent == 0:
					subprocess.call("./on_fall.sh", shell=True)	# speech output to user
					fall_msg_sent = 1	# don't send another

				has_fallen = 1		# triggers get help text **********
				above_count = 0		# reset count

			iter = iter + 1

			if iter % 200 == 0:
				fall_msg_sent = 0	# reset it
