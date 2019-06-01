#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from subprocess import call
from picamera import PiCamera

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Motor 1 uses Pin 22, Pin 18, Pin 16 
Motor1A = 31
Motor1B = 33
Motor1E = 35
 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

# Motor 2 uses Pin 15, Pin 13, Pin 11
Motor2A = 11
Motor2B = 13
Motor2E = 15

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

# Defining camera
camera = PiCamera()

# Servo motor uses Pin 12
GPIO.setup(12,GPIO.OUT)

def servoUp():
	print("Camera Focusing Up")
	p = GPIO.PWM(12,50)
	p.start(0)
	p.ChangeDutyCycle(4.5)
	sleep(1)
	p.stop()

def servoDown():
	print("Camera Facing Down")
	p = GPIO.PWM(12,50)
	p.start(0)
	p.ChangeDutyCycle(3)
	sleep(1)
	p.stop()


def forward(dur):
	print("Moving Forward")
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor1E,GPIO.HIGH)
	GPIO.output(Motor2A,GPIO.LOW)
	GPIO.output(Motor2B,GPIO.HIGH)
	GPIO.output(Motor2E,GPIO.HIGH)
	sleep(dur)
	GPIO.output(Motor1E,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.LOW)
	return

def backward(dur):
	print("Moving Backward")
	GPIO.output(Motor1A,GPIO.LOW)
	GPIO.output(Motor1B,GPIO.HIGH)
	GPIO.output(Motor1E,GPIO.HIGH)
	GPIO.output(Motor2A,GPIO.HIGH)
	GPIO.output(Motor2B,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.HIGH)
	sleep(dur)
	GPIO.output(Motor1E,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.LOW)
	return

def uTurn(dur):
	print("Taking U-Turn")
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor1E,GPIO.HIGH)	
	GPIO.output(Motor2A,GPIO.HIGH)
	GPIO.output(Motor2B,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.HIGH)
	sleep(dur)
	GPIO.output(Motor1E,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.LOW)
	return

def turnRight(dur):
	print("Turning Right")
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor1E,GPIO.HIGH)
	sleep(dur)
	GPIO.output(Motor1E,GPIO.LOW)
	return

def turnLeft(dur):
	print("Turning Left")
	GPIO.output(Motor2A,GPIO.LOW)
	GPIO.output(Motor2B,GPIO.HIGH)
	GPIO.output(Motor2E,GPIO.HIGH)
	sleep(dur)
	GPIO.output(Motor2E,GPIO.LOW)
	return

def stopMotors():
	GPIO.output(Motor1E,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.LOW)

def getData():
	motion = input("Next Step ")
	return motion

def captureVideo(dur):
	print("Showing Video")
	camera.rotation = 180
	camera.start_preview()
	sleep(dur)
	camera.stop_preview()

def capturePicture():
	print("Taking Picture")
	camera.resolution = (2592, 1944)
	camera.framerate = 15
	camera.rotation = 180
	camera.start_preview()
	sleep(2)
	camera.capture('/home/pi/pyth/picam.jpg')
	camera.stop_preview()

def speaking(text):
	call([cmd+text],shell=True)
	#call([cmd+text+"'"],shell=True)
	return

###Defining Google speech (using internet)
cmd="./speech.sh "
#cmd="sudo su - pi -c'/home/pi/pyth/speech.sh "

speaking("Hey Welcome, Lets Start")
motion = input('''Enter <Direction/Camera><Duration>
Direction: F/B/L/R/T (X for exit)
Duration: Less than 10 in seconds
Camera: V/P
Camera Face: U/D
Enter S to repeat
''')

###First motion
start=list(motion)
last_motion=motion
try:
	dur = int(start[1])
except IndexError:
	dur = 1

###Continuous motion depending on user input
while (start[0] != 'X' and start[0] != 'x'):
###Forward step
	if (start[0] == 'F' or start[0] == 'f'):
		speaking("Hey Moving Forward")
		forward(dur)

###Backward step
	elif (start[0] == 'B' or start[0] == 'b'):
		speaking("Hey Moving Backwards")
		backward(dur)

###Moving to left
	elif (start[0] == 'L' or start[0] == 'l'):
		speaking("Hey Turning Left")
		turnLeft(dur)

###Moving to right
	elif (start[0] == 'R' or start[0] == 'r'):
		speaking("Hey Turning Right")
		turnRight(dur)

###Taking U-Turn
	elif (start[0] == 'T' or start[0] == 't'):
		speaking("Hey Taking U Turn")
		uTurn(dur)

###Camera Handling
	elif (start[0] == 'v' or start[0] == 'V'):
		speaking("Hey Showing Video")
		captureVideo(dur)

	elif (start[0] == 'p' or start[0] == 'P'):
		speaking("Hey Taking Picture")
		capturePicture()

###Tilt Camera
	elif (start[0] == 'u' or start[0] == 'U'):
		speaking("Hey Camera Focusing Up")
		servoUp()

	elif (start[0] == 'd' or start[0] == 'D'):
		speaking("Hey Camera Facing Down")
		servoDown()

###Handling incorrect option from user
	else:
		speaking("Hey Incorrect Option Please Try Again")
		print("Incorrect Option, Try Again!!")

###Getting next input from user
	stopMotors()
	motion = getData()
	start=list(motion)
	if (start[0] == 's' or start[0] == 'S'):
		start=list(last_motion)
		try:
			dur = int(start[1])
		except IndexError:
			if (start[0] == 'V' or start[0] == 'v'):
				dur = 5
			else:
				dur = 1
	else:
		last_motion=motion		
###Handling duration exception
		try:
			dur = int(start[1])
		except IndexError:
			if (start[0] == 'V' or start[0] == 'v'):
				dur = 5
			else:
				dur = 1

###Ending steps
speaking("Hey Sorry To See You Go")
print ("See You Next Time!!!")		
GPIO.cleanup()

