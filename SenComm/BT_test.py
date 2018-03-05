import serial
import math
from twilio.rest import Client		# to send texts (for now)

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

file_out = open('mag_data.txt', 'w')	# File to write mag data
file_out.write('Time,Magnitude\n')

# credentials
acct_sid = "ACbe73c35f1e1483a0a3c53fcc9dc815ad"
token = "f88deacaa9f98732c4d66a977996bd34"

client = Client(acct_sid, token)

fall_msg_sent = 0	# to not overload node red with messages

# Get data
while iter < 5000:
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
					file_falls_out = open('falls.txt', 'w')         # File to log falls
					file_falls_out.write('FALL!!!')
                                	file_falls_out.close()
					fall_msg_sent = 1	# don't send another

				print 'FALL!!!!!'	# Alert!!!
				has_fallen = 1		# triggers get help text **********
				above_count = 0		# reset count

			file_out.write('%d,%f\n' % (iter, vect_mag))	# write data to file

			if has_fallen == 1:	# Get help text **********
				# Send "get help!" text
				response = client.messages.create(
					to = "+15129471505",
					from_ = "+15124569474",
					body = "Help! I've fallen and I can't get up!"
					)
				has_fallen = 0		# reset control for text


			#mags.append(vect_mag)
			#time.append(start)

			iter = iter + 1

			if iter % 100 == 0:
				print iter
				fall_msg_sent = 0	# reset it

			#print a_x, a_y, a_z

file_out.close()	# make sure to close
