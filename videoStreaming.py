#!/usr/bin/python3

import cv2
import datetime

print("Press TAB to capture pic; ESC to quit")

cam = cv2.VideoCapture(0)

cv2.namedWindow("Frame")

while True:
    ret, frame = cam.read()
    frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_180)
    cv2.imshow("Frame", frame)
    #cv2.flip(frame, flipCode=-1)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 9:
        # TAB pressed
        img_name = "image.jpg"
        now = datetime.datetime.now()
        cv2.imwrite(img_name, frame)
        print("image.jpg saved at", now.strftime("%Y-%m-%d %H:%M:%S"))

cam.release()

cv2.destroyAllWindows()
