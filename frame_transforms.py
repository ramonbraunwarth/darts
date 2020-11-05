#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
# import matplotlib.pyplot as plt
import time 



def transform_frame(frame, selector_key = 'none'):
    '''
    INPUT: cameraframe, selector key as str
    OUTPUT: cameraframe transformed according to transformation chosed by selector key

    Currently supported choices: 
    - 'none'    : Return input frame
    - 'green'   : Set green mask for dart board
    - 'red'     : Set red mask for dart board
    - 'canny'   : Edge detection with cv2.Canny

    Use constant TRANSFORM_SELECTOR_KEY in code below
    '''

    # No transformation for default value
    if selector_key == 'none':
        return frame

    # Transformation from dartboard_detector for certain colors (green, red)
    if selector_key in ('green','red'):
        if selector_key == 'green':
            # CONST variables for green detection
            hue_min = 90   
            hue_max = 150
            SV_threshold = 60 # Set lower threshold for saturation and value (lumination) in mask
        if selector_key == 'red':
            # CONST variables for green detection
            hue_min = 0  
            hue_max = 20
            SV_threshold = 80 # Set lower threshold for saturation and value (lumination) in mask

        # Set a blur with a Gaussian smoothing kernel
        BLUR = (5,5) 
        blurred_frame = cv2.GaussianBlur(frame,BLUR,0)

        # convert to HSV (Hue, Saturation, Value: Converted from RGB)
        HSV_blurred_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        # Extract areas with desired color (hue)
        threshold_low = int(hue_min /255. * 180)
        threshold_high = int(hue_max /255. * 180)

        # Set HSV limits for the mask:
        # TRY OUT DIFFERENT VALUES FOR S AND V TO GET A BETTER RESULT
        mask_limit_low  = np.array([threshold_low, SV_threshold, SV_threshold],np.uint8)
        mask_limit_high = np.array([threshold_high, 255, 255],np.uint8)

        return cv2.inRange(HSV_blurred_frame, mask_limit_low, mask_limit_high)
        
    if selector_key == 'edges':
        return cv2.Canny(frame, 100, 200)

    if selector_key == 'redandgreen':  #Probably not the cleanest implementation (key and recursion), +++TBI
        #CONST value for below, originally called DETECTION_STRUCTURING_ELEMENT: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html 
        DETECTION_KERNEL = (100,100)

        #Combine red and green frame
        redgreen_frame = transform_frame('red') + transform_frame('green')

        #Closing with cv2.morphologyEx and argument cv2.MORPH_CLOSE (remove noisy gaps in detected circles)
        closing_kernel = np.ones(DETECTION_KERNEL,np.uint8)
        return cv2.morphologyEx(redgreen_frame, cv2.MORPH_CLOSE, closing_kernel)

        

    # If no selector key matches, return input frame
    return frame













# Key to choose transformation in transform_frame() above
TRANSFORMATION_SELECTOR_KEY = 'redandgreen'


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



# show video (in extra window), stop by pressing q
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    #The following line would change the RGB frame to a greyscale. We need RGB for the detection of the board.
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize window
    frame = cv2.resize(frame, (500, 300))

    # FPS CALCULATION AND DISPLAY
    # time when we finish processing for this frame 
    new_frame_time = time.time() 
    fps = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time 
    fps = int(fps) 
    # converting the fps to string so that we can display it on frame 
    # by using putText function 
    fps = str(fps) 
    # puting the FPS count on the frame 
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 


    #Transform the frame according to some rule specified with second argument
    frame = transform_frame(frame, TRANSFORMATION_SELECTOR_KEY) 

    # Display the resulting frame
    cv2.imshow('frame',frame)
    # key = cv2.waitKey(0) & 0xFF

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()






