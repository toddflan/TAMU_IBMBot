import serial

ser = serial.Serial('/dev/rfcomm0', 115200)

#for i in range (0,25):
#	result = ord(ser.read())
#	print hex(result)
#	if result == 0x55:
#		print "Winner"

while True:
	result = ord(ser.read())
	if result == 0x55:
		data = []
		data.append(result)
		for i in range(1,10):
			data.append(ord(ser.read()))
		if data[1] == 0x51:
			a_x = (data[3] << 8 | data[2])#/32768.0*16
			a_y = (data[5] << 8 | data[4])#/32768.0*16
			a_z = (data[7] << 8 | data[6])#/32768.0*16
			print a_x, a_y, a_z
