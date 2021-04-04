#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import matplotlib.pyplot as plt


def get_board_fotos():
    '''
    Starts Video from Camera 0, exit with 'esc', take picture with 'space'
    '''
    cv2.namedWindow("dartboard")
    
    img_counter = 0
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("dartboard", frame)
    
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = "dartboard_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
     
cam = cv2.VideoCapture(1)
get_board_fotos()   
cam.release()
cv2.destroyAllWindows()


# load image of dartboard, manually taken from video stream with code above
board_1 = cv2.imread('dartboard_0.png', 1)

# convert image to HSV
board_1_hsv = cv2.cvtColor(board_1, cv2.COLOR_BGR2HSV)

# get green and red mask
mask_green = cv2.inRange(board_1_hsv, (36, 25, 25), (86, 255,255))
mask_red = cv2.inRange(board_1_hsv, (36, 25, 25), (86, 255,255))


imask = mask>0
green = np.zeros_like(board_1, np.uint8)
green[imask] = board_1[imask]
plt.imshow(green)

# plot image & extracted regions
plt.imshow(board_1[:,:,::-1])
# alternative plotting with cv2, doesn't work well on Spyder though
cv2.imshow('image', board_1)
cv2.waitKey(0)
cv2.destroyAllWindows()
