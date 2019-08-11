#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import curses

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor 1 uses Pin 22, Pin 18, Pin 16 
Motor1A = 6
Motor1B = 13
Motor1E = 19
 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

# Motor 2 uses Pin 15, Pin 13, Pin 11
Motor2A = 22
Motor2B = 27
Motor2E = 17

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

pwm1=GPIO.PWM(19,100)
pwm2=GPIO.PWM(17,100)

# Setting up LEDs
leftRED=23  
rightRED=25

GPIO.setup(leftRED,GPIO.OUT)
GPIO.setup(rightRED,GPIO.OUT)

# Servo Motors use Pin 32 and 36
S_UD = 12
S_LR = 16

GPIO.setup(S_UD,GPIO.OUT)
GPIO.setup(S_LR,GPIO.OUT)

# Ultrasonic sensor use Pin 12 and 18
GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


## Functions start

def backward1(dur):
    print("Moving Back")
    pwm1.start(duty)
    pwm2.start(duty)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    time.sleep(dur)
    stopMotors()
    pwm1.stop()
    pwm2.stop()
    return

def backward2():
    print("Moving Back")
    pwm1.start(duty)
    pwm2.start(duty)
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
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)
    time.sleep(dur)
    stopMotors()
    pwm1.stop()
    pwm2.stop()
    return
    
def forward2():
    print("Moving Front")
    pwm1.start(duty)
    pwm2.start(duty)
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

def turnRight1(dur):
    print("Turning Right")
    GPIO.output(leftRED,GPIO.LOW)
    GPIO.output(rightRED,GPIO.HIGH)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    time.sleep(dur)
    GPIO.output(rightRED,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.LOW)
    return
    
def turnRight2():
    print("Turning Right")
    GPIO.output(leftRED,GPIO.LOW)
    GPIO.output(rightRED,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.LOW)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

def turnLeft1(dur):
    print("Turning Left")
    GPIO.output(rightRED,GPIO.LOW)
    GPIO.output(leftRED,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    time.sleep(dur)
    GPIO.output(leftRED,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
    return
    
def turnLeft2():
    print("Turning Left")
    GPIO.output(rightRED,GPIO.LOW)
    GPIO.output(leftRED,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

def stopMotors():
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)

def lightOff():
    GPIO.output(leftRED,GPIO.LOW)
    GPIO.output(rightRED,GPIO.LOW)

def servoUp():
    print("Camera Focusing Up")
    p = GPIO.PWM(S_UD,50)
    p.start(0)
    p.ChangeDutyCycle(1)
    time.sleep(1)
    p.stop()

def servoDown():
    print("Camera Facing Down")
    p = GPIO.PWM(S_UD,50)
    p.start(0)
    p.ChangeDutyCycle(4.5)
    time.sleep(1)
    p.stop()

def servoLeft():
    print("Camera Moving Left")
    p = GPIO.PWM(S_LR,50)
    p.start(0)
    p.ChangeDutyCycle(4.5)
    time.sleep(1)
    p.stop()
    return dc

def servoRight():
    print("Camera Moving Right")
    p = GPIO.PWM(S_LR,50)
    p.start(0)
    p.ChangeDutyCycle(1.5)
    time.sleep(1)
    p.stop()
    return dc

def servoReset():
    p1 = GPIO.PWM(S_LR,50)
    p2 = GPIO.PWM(S_UD,50)
    p1.start(0)
    p2.start(0)
    p1.ChangeDutyCycle(3)
    p2.ChangeDutyCycle(3)
    time.sleep(1)
    p1.stop()
    p2.stop()
    return dc

def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2

    return distance


## Functions end
dc = 3
try:
    duty = int(input("Enter speed of motor from 50%(min) to 100%(max) : default 75"))
except ValueError:
    duty = 75

motion = input('''Instructions:
Arrow keys for continuous movement
F/B/L/R for step movement
C for Camera movement
D for Distance from obstruction

Press K to start
Enter X to exit
''')

if (motion != 'k' and motion != 'K' and motion != 'X' and motion != 'x'):
    print("Wrong Option...Exiting")
    motion='X'
###Continuous motion depending on user input
while (motion != 'X' and motion != 'x'):

    if (motion == 'K' or motion == 'k'):
    ###Instant key response
        screen =curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        try:
                while True:
                    char = screen.getch()
                    if char == ord('x'):
                        break
                    elif char == curses.KEY_UP:
                        lightOff()
                        pwm1.stop()
                        pwm2.stop()
                        forward2()
                    elif char == ord('f'):
                        lightOff()
                        forward1(1)
                    elif char == curses.KEY_DOWN:
                        lightOff()
                        pwm1.stop()
                        pwm2.stop()
                        backward2()
                    elif char == ord('b'):
                        lightOff()
                        backward1(1)
                    elif char == curses.KEY_RIGHT:
                        pwm1.stop()
                        pwm2.stop()
                        turnRight2()
                    elif char == ord('r'):
                        turnRight1(1)
                    elif char == curses.KEY_LEFT:
                        pwm1.stop()
                        pwm2.stop()
                        turnLeft2()
                    elif char == ord('l'):
                        turnLeft1(1)
                    elif char == ord('c'):
                        if dc == 4.5:
                            servoReset()
                            dc = 3
                        elif dc == 3:
                            servoRight()
                            dc = 1.5
                        elif dc == 1.5:
                            servoLeft()
                            dc = 4.5
                    elif char == ord('d'):
                        dist = distance()
                        print ("Measured Distance = %.1f cm" % dist)
                    elif char == 10:
                        lightOff()
                        stopMotors()
                        pwm1.stop()
                        pwm2.stop()
                        servoReset()
                        dc = 3
        finally:
            curses.nocbreak(); screen.keypad(0); curses.echo()
            curses.endwin()
            motion='X'


###Ending steps
print ("See You Next Time!!!")        
pwm1.stop()
pwm2.stop()
servoReset()
lightOff()
GPIO.cleanup()

