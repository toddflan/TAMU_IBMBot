#
# Get connected to wifi using creds sent from app
#

#---Imports-------------------------------------------------

import bluetooth	# communication with app
import socket
from wifi import Cell, Scheme	# to connect wifi

#-----------------------------------------------------------

#---Connect to app------------------------------------------
# **********************************************************
# From circuitdigest.com controlling raspberry pi gpio using...
# ...android app over bluetooth
# **********************************************************

# Get rfcomm
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Setup server
port = 1
server.bind(("", bluetooth.PORT_ANY))
server.listen(1)

# UUID for serial comms
my_uuid = "00001101-0000-1000-8000-00805F9B34FB"

# Let app know we're ready to party
bluetooth.advertise_service( server, "David",
	service_id = my_uuid,
	service_classes = [ my_uuid, bluetooth.SERIAL_PORT_CLASS ],
	profiles = [ bluetooth.SERIAL_PORT_PROFILE ]
	)

# Connect to phone
client, address = server.accept()
print "Accepted connection from ", address

# Define network name (ssid) and password (pwd) strings
ssid = ""
pwd = ""

#-----------------------------------------------------------

#---Connect to wifi-----------------------------------------

wifi_is_found = 0	# boolean for finding wifi

while (wifi_is_found == 0):
	# Get wifi creds over BT
	recvd_data = client.recv(100)		# 100 should be plenty for wifi name, pwd
	ssid, pwd = recvd_data.split(",", 1)	# split the string at ','

	print ssid, pwd		# testing **************************

	cell_list = Cell.all('wlan0')	# gets list of networks

	for cell in cell_list:		# find right one
		if cell.ssid == ssid:
			wifi_is_found = 1		# found it
			break

	if wifi_is_found != 1:
		client.send("Error: wifi not found")	# send error, retry sending creds
	else:
		print cell		# connect to wifi network
		scheme = Scheme.for_cell('wlan0', 'home', cell, pwd)
		scheme.save()
		scheme.activate()

#-----------------------------------------------------------

#---Send IP address to app----------------------------------

# Open a socket to get device ip and save it
# FROM STACK EXCHANGE ********************
# stackoverflow, questions, finding local ip addresses using python stdlib
# ****************************************
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
my_ip = s.getsockname()[0]	# save ip
s.close()	# close socket

print my_ip		# print IP so server can use it later
client.send(my_ip)	# send IP to app

#-----------------------------------------------------------

#---Clean up------------------------------------------------

client.close()		# close both
server.close()

#-----------------------------------------------------------
