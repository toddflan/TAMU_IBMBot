import serial
import math

# Function for decoding accelerometer data
def getAccel(num):
	if (num & 0x8000) == 0x8000:	# if MSB is 1 (negative number)
		return (num - 65536) / 32768.0 * 16	# convert twos complement to negative integer
	else:
		return num / 32768.0 * 16

# Serial connection
ser = serial.Serial('/dev/rfcomm0', 115200)

#time = []	# for plotting
#mags = []

start = 0
iter = 0

file_out = open('mag_data.txt', 'w')	# File to write mag data
file_out.write('Time,Magnitude\n')

# Get data
while iter < 10000:
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

			file_out.write('%d,%f\n' % (start, vect_mag))	# write data to file

			#mags.append(vect_mag)
			#time.append(start)
			start = start + 1

			iter = iter + 1

			#if vect_mag > 2:
			#	print vect_mag

			#print a_x, a_y, a_z

#plt.plot(time, mags)
#plt.draw()

file_out.close()	# make sure to close
