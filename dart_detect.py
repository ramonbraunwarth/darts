#!/usr/bin/env python
# coding: utf-8



import cv2
import numpy as np
import matplotlib.pyplot as plt


cap = cv2.VideoCapture(0)

# get width
width = cap.get(3)
print('width: ' + str(width))
# get height
height = cap.get(4)
print('height: ' + str(height))

#set wanted width and heigth
#ret = cap.set(3, width/4)
#ret = cap.set(4, height/4)

# check width
width = cap.get(3)
print('new width: ' + str(width))
# check height
height = cap.get(4)
print('new height: ' + str(height))


# show video (in extra window), stop by pressing q
#cv2.startWindowThread()      # else window won't close when q is pressed
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    key = cv2.waitKey(0) & 0xFF
#    if key == ord("q"):
#        break
    if cv2.waitKey(0) == ord('q'):
        break
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()






