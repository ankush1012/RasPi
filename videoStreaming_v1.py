#!/usr/bin/python3

# Import packages
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

print("Press q to switch off Video Camera")
# Set up camera constants
#IM_WIDTH = 1280
#IM_HEIGHT = 720
IM_WIDTH = 640    #Use smaller resolution for
IM_HEIGHT = 480   #slightly faster framerate

# Initialize Picamera and grab reference to the raw capture
camera = PiCamera()
camera.resolution = (IM_WIDTH,IM_HEIGHT)
camera.rotation = 180
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
rawCapture.truncate(0)

for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
    image = frame.array
    cv2.imshow("Frame", image)

# Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break
    if cv2.waitKey(1) == ord('p'):
        cv2.imwrite('home/pi/image.jpg',image)

    rawCapture.truncate(0)

camera.close()

cv2.destroyAllWindows()

