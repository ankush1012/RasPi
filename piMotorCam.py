#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera
from multiprocessing import Process

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Motor 1 uses Pin 22, Pin 18, Pin 16 
Motor1A = 31
Motor1B = 33
Motor1E = 35
 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.output(Motor1E,GPIO.LOW)

# Defining camera
camera = PiCamera()

def forward():
	print("Starting forward")
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor1E,GPIO.HIGH)
	sleep(5)
	GPIO.output(Motor1E,GPIO.LOW)
	print("Ending forward")

def captureVideo():
	print("Starting captureVideo")
	camera.rotation = 180
	camera.start_preview()
	sleep(5)
	camera.stop_preview()
	print("Ending captureVideo")
	return

if __name__ == '__main__':
	p1 = Process(target=captureVideo)
	p1.start()
	p2 = Process(target=forward)
	p2.start()
	p1.join()
	p2.join()

	GPIO.cleanup()

