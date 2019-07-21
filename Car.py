#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
import curses

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
Motor2A = 15
Motor2B = 13
Motor2E = 11

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

pwm1=GPIO.PWM(35,100)
pwm2=GPIO.PWM(11,100)

# Setting up LEDs
leftRED=16
WHITE=18
rightRED=22
GPIO.setup(leftRED,GPIO.OUT)
GPIO.setup(WHITE,GPIO.OUT)
GPIO.setup(rightRED,GPIO.OUT)

# Servo Motors use Pin 32 and 36
S_UD = 32
S_LR = 36

GPIO.setup(S_UD,GPIO.OUT)
GPIO.setup(S_LR,GPIO.OUT)

## Functions start

def backward1(dur):
    print("Moving Back")
    pwm1.start(duty)
    pwm2.start(duty)
    GPIO.output(WHITE,GPIO.HIGH)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    sleep(dur)
    GPIO.output(WHITE,GPIO.LOW)
    stopMotors()
    pwm1.stop()
    pwm2.stop()
    return

def backward2():
    print("Moving Back")
    pwm1.start(duty)
    pwm2.start(duty)
    GPIO.output(WHITE,GPIO.HIGH)
    GPIO.output(leftRED,GPIO.LOW)
    GPIO.output(rightRED,GPIO.LOW)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

def forward1(dur):
    print("Moving Front")
    pwm1.start(duty)
    pwm2.start(duty)
    GPIO.output(WHITE,GPIO.HIGH)
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)
    sleep(dur)
    GPIO.output(WHITE,GPIO.LOW)
    stopMotors()
    pwm1.stop()
    pwm2.stop()
    return
    
def forward2():
    print("Moving Front")
    pwm1.start(duty)
    pwm2.start(duty)
    GPIO.output(WHITE,GPIO.HIGH)
    GPIO.output(leftRED,GPIO.LOW)
    GPIO.output(rightRED,GPIO.LOW)
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

def turnRight1(dur):
    print("Turning Right")
    GPIO.output(rightRED,GPIO.HIGH)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    sleep(dur)
    GPIO.output(rightRED,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.LOW)
    return
    
def turnRight2():
    print("Turning Right")
    GPIO.output(rightRED,GPIO.HIGH)
    GPIO.output(WHITE,GPIO.LOW)
    GPIO.output(leftRED,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

def turnLeft1(dur):
    print("Turning Left")
    GPIO.output(leftRED,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    sleep(dur)
    GPIO.output(leftRED,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
    return
    
def turnLeft2():
    print("Turning Left")
    GPIO.output(leftRED,GPIO.HIGH)
    GPIO.output(WHITE,GPIO.LOW)
    GPIO.output(rightRED,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

def stopMotors():
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)

def servoUp():
    print("Camera Focusing Up")
    p = GPIO.PWM(S_UD,50)
    p.start(0)
    p.ChangeDutyCycle(1)
    sleep(1)
    p.stop()

def servoDown():
    print("Camera Facing Down")
    p = GPIO.PWM(S_UD,50)
    p.start(0)
    p.ChangeDutyCycle(4.5)
    sleep(1)
    p.stop()

def servoLeft():
    print("Camera Moving Left")
    p = GPIO.PWM(S_LR,50)
    p.start(0)
    p.ChangeDutyCycle(4.5)
    sleep(1)
    p.stop()

def servoRight():
    print("Camera Moving Right")
    p = GPIO.PWM(S_LR,50)
    p.start(0)
    p.ChangeDutyCycle(1.5)
    sleep(1)
    p.stop()

def servoReset():
    print("Camera resetting")
    p1 = GPIO.PWM(S_LR,50)
    p2 = GPIO.PWM(S_UD,50)
    p1.start(0)
    p2.start(0)
    p1.ChangeDutyCycle(3)
    p2.ChangeDutyCycle(3)
    sleep(1)
    p1.stop()
    p2.stop()

def getData():
    motion = input("Next Step ")
    return motion

## Functions end

duty = int(input("Enter speed of motor from 50%(min) to 100%(max)"))

motion = input('''Instructions:
Press K to use arrow keys for directions OR
Use format <Direction><Duration> 
Direction: F/B/L/R 
Press C to direct camera
Enter S to repeat
Enter X to exit
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

    if (start[0] == 'K' or start[0] == 'k'):
    ###Instant key response
        screen =curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        try:
                while True:
                    print("Press q to exit arrow based operation")
                    char = screen.getch()
                    if char == ord('q'):
                        break
                    elif char == curses.KEY_UP:
                        pwm1.stop()
                        pwm2.stop()
                        forward2()
                    elif char == curses.KEY_DOWN:
                        pwm1.stop()
                        pwm2.stop()
                        backward2()
                    elif char == curses.KEY_RIGHT:
                        pwm1.stop()
                        pwm2.stop()
                        turnRight2()
                    elif char == curses.KEY_LEFT:
                        pwm1.stop()
                        pwm2.stop()
                        turnLeft2()
                    elif char == 10:
                        stopMotors()
                        pwm1.stop()
                        pwm2.stop()
        finally:
            curses.nocbreak(); screen.keypad(0); curses.echo()
            curses.endwin()    

    elif (start[0] == 'C' or start[0] == 'c'):
    ###Instant key usage for setting Camera direction
        screen =curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        try:
            while True:
                print("Press q to exit arrow based operation")
                char = screen.getch()
                if char == ord('q'):
                    break
                elif char == curses.KEY_UP:
                    servoUp()
                elif char == curses.KEY_DOWN:
                    servoDown()
                elif char == curses.KEY_RIGHT:
                    servoRight()
                elif char == curses.KEY_LEFT:
                    servoLeft()
                elif char == 10:
                    servoReset()
        finally:
            curses.nocbreak(); screen.keypad(0); curses.echo()
            curses.endwin()

    else:
    ###Forward step
        if (start[0] == 'F' or start[0] == 'f'):
            forward1(dur)
    
    ###Backward step
        elif (start[0] == 'B' or start[0] == 'b'):
            backward1(dur)
    
    ###Moving to left
        elif (start[0] == 'L' or start[0] == 'l'):
            turnLeft1(dur)
    
    ###Moving to right
        elif (start[0] == 'R' or start[0] == 'r'):
            turnRight1(dur)
    
    ###Handling incorrect option from user
        else:
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
            dur = 1
    else:
        last_motion=motion        
###Handling duration exception
        try:
            dur = int(start[1])
        except IndexError:
            dur = 1

###Ending steps
print ("See You Next Time!!!")        
pwm1.stop()
pwm2.stop()
GPIO.cleanup()

