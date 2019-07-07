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

def forward1(dur):
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

def forward2():
    print("Moving Forward")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

def backward1(dur):
    print("Moving Backward")
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)
    sleep(dur)
    stopMotors()
    return
    
def backward2():
    print("Moving Backward")
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

def turnRight1(dur):
    print("Turning Right")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    sleep(dur)
    GPIO.output(Motor1E,GPIO.LOW)
    return
    
def turnRight2():
    print("Turning Right")
    GPIO.output(Motor2E,GPIO.LOW)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

def turnLeft1(dur):
    print("Turning Left")
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    sleep(dur)
    GPIO.output(Motor2E,GPIO.LOW)
    return
    
def turnLeft2():
    print("Turning Left")
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

def stopMotors():
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)

def getData():
    motion = input("Next Step ")
    return motion

motion = input('''Instructions:
Press K to use arrow keys for directions OR
Use format <Direction><Duration> 
Direction: F/B/L/R 
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
                        forward2()
                    elif char == curses.KEY_DOWN:
                        backward2()
                    elif char == curses.KEY_RIGHT:
                        turnRight2()
                    elif char == curses.KEY_LEFT:
                        turnLeft2()
                    elif char == 10:
                        stopMotors()
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
GPIO.cleanup()

