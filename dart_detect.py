#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
import time 





cap = cv2.VideoCapture(0)

# get width
width = cap.get(3)
print('width: ' + str(width))
# get height
height = cap.get(4)
print('height: ' + str(height))

#set wanted width and heigth
# ret = cap.set(3, width/4)
# ret = cap.set(4, height/4)

# check width
width = cap.get(3)
print('new width: ' + str(width))
# check height
height = cap.get(4)
print('new height: ' + str(height))

# used to record the time when we processed last frame 
prev_frame_time = 0
  
# used to record the time at which we processed current frame 
new_frame_time = 0

# In[3]:


# show video (in extra window), stop by pressing q
cv2.startWindowThread()      # else window won't close when q is pressed
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize (new)
    gray = cv2.resize(gray, (500, 300)) 

    font = cv2.FONT_HERSHEY_SIMPLEX 

    # time when we finish processing for this frame 
    new_frame_time = time.time() 
    fps = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time 
    fps = int(fps) 
  
    # converting the fps to string so that we can display it on frame 
    # by using putText function 
    fps = str(fps) 
  
    # puting the FPS count on the frame 
    cv2.putText(gray, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 


    # Display the resulting frame
    cv2.imshow('frame',gray)
    # key = cv2.waitKey(0) & 0xFF
#    if key == ord("q"):
#        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()






