import serial
import time
import struct
import create # Nice library I found with all the Create code you could want
              # currently only using it for sensor code

connection = None
velocity = 0
rotation = 0

# Motor constants
VELOCITYCHANGE = 200
ROTATIONCHANGE = 300

# Command codes
PASSIVE = '128'
SAFE = '131'
FULL = '132'
CLEAN = '135'
DOCK = '143'
BEEP = '140 3 1 64 16 141 3'
RESET = '7'
BUMPSENSOR = '142 7'
CHARGE = '142 21'

def sendCommandASCII(command):
	cmd = ""
	for v in command.split():
		cmd += chr(int(v))

	sendCommandRaw(cmd)

def sendCommandRaw(command):
	global connection

	try:
		if connection is not None:
			connection.write(command)
		else:
			print "not connected"
	except serial.SerialException:
		print "lost connection"

	print ' '.join([ str(ord(c)) for c in command ])

# Connects to robot through serial USB
def Connect():
	global connection

	# Hard coded for Nick S MacBook
	# MUST be changed for PC/other computers
	# port = "/dev/tty.usbserial-DA017TKR"

	port = "COM3"

	try:
		connection = serial.Serial(port, baudrate=115200, timeout=1)
		print "Connected"
		return True
	except serial.SerialException:
		print "Failed"
		return False

# Drive straight for specified time t
# Set direction d to either 1 (forward) or -1 (backward)
def DriveStraight(d, t):
	velocity = d * VELOCITYCHANGE
	vr = velocity
	vl = velocity
	cmd = struct.pack(">Bhh", 145, vr, vl)
	sendCommandRaw(cmd)

	time.sleep(t)

	velocity = 0
	vr = 0
	vl = 0
	cmd = struct.pack(">Bhh", 145, vr, vl)
	sendCommandRaw(cmd)

# Rotate 90 degrees in specified direction d
# -1 (clockwise) or 1 (counter-clockwise)
def Rotate(d):
	rotation = d * ROTATIONCHANGE
	vr = rotation/2
	vl = -rotation/2
	cmd = struct.pack(">Bhh", 145, vr, vl)
	sendCommandRaw(cmd)

	time.sleep(1.5)

	vr = 0
	vl = 0
	cmd = struct.pack(">Bhh", 145, vr, vl)
	sendCommandRaw(cmd)

# Drive in a square (approx. 1 ft x 1 ft)
def Square():
	DriveStraight(1, 1)
	Rotate(1)
	DriveStraight(1, 1)
	Rotate(1)
	DriveStraight(1, 1)
	Rotate(1)
	DriveStraight(1, 1)
	sendCommandASCII(BEEP)

# Connects and puts robot in proper mode to 
# receive commands
def Start():
	# Connect to robot
	while(not Connect()):
		continue

	# Sends passive then full
	# Sleeps are to make sure commands are received
	# Probably can be shortened for better efficiency
	time.sleep(0.5)
	sendCommandASCII(PASSIVE)
	time.sleep(2)
	#sendCommandASCII(FULL)
	time.sleep(1)

r = create.Create(3)

d = r.sensors()

print d[create.LEFT_BUMP]
print d[create.RIGHT_BUMP]

r.close()
