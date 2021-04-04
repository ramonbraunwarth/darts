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

# start video stream, take fotos and close window
cam = cv2.VideoCapture(1)
get_board_fotos()   
cam.release()
cv2.destroyAllWindows()


# load image of dartboard, manually taken from video stream with code above
board_1 = cv2.imread('dartboard_0.png', 1)

# convert image to HSV
board_1_hsv = cv2.cvtColor(board_1, cv2.COLOR_BGR2HSV)

# get green and red mask (2 for red as red goes from 170-180 and 0-10)
mask_green = cv2.inRange(board_1_hsv, (36, 25, 25), (86, 255,255))
mask_red_1 = cv2.inRange(board_1_hsv, (170, 25, 25), (180, 255,255))
mask_red_2 = cv2.inRange(board_1_hsv, (0, 25, 25), (1, 255,255))
mask_red = mask_red_1 + mask_red_2

# visualize green and red masks
imask = mask_green>0
green = np.zeros_like(board_1, np.uint8)
green[imask] = board_1[imask]
plt.imshow(green)

imask = mask_red>0
red = np.zeros_like(board_1, np.uint8)
red[imask] = board_1[imask]
plt.imshow(red)

# add both masks
mask = mask_green + mask_red
imask = mask>0
comb = np.zeros_like(board_1, np.uint8)
comb[imask] = board_1[imask]
plt.imshow(comb[:,:,::-1])

# convert the image to a gray scale, binary image to use cv2.findContours()
comb = cv2.cvtColor(comb, cv2.COLOR_BGR2GRAY)
comb[imask] = 255
plt.imshow(comb, cmap='gray')

# get contours
# retrieval methods: cv2.RETR_EXTERNAL, cv2.RETR_TREE
contours, hierarchy = cv2.findContours(comb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
plt.imshow(cv2.drawContours(np.ones_like(comb), contours, -1, (0,255), 3), cmap='gray')

# cluster contours or outlier detection of contour-midpoints to find dartboard?

# draw rectangles for bigger contours


# plot image & extracted regions
plt.imshow(board_1[:,:,::-1])
# alternative plotting with cv2, doesn't work well on Spyder though
cv2.imshow('image', board_1)
cv2.waitKey(0)
cv2.destroyAllWindows()
