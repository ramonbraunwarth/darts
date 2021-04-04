#!/usr/bin/env python
# coding: utf-8


class Dartboard_Detector:

	ENV = {
	        'DARTBOARD_SHAPE' : (1000,1000),

	        'DETECTION_BLUR' : (5,5),

	        #HSV hue intervall for detection of green fields 
	        'DETECTION_GREEN_LOW' : 100,
	        'DETECTION_GREEN_HIGH' : 140,
	        #HSV hue intervall for detection of red fields 
	        'DETECTION_RED_LOW' : 0,
	        'DETECTION_RED_HIGH' : 20,

	        'DETECTION_STRUCTURING_ELEMENT' : (100,100),
	        'DETECTION_BINARY_THRESHOLD_MIN' : 127,
	        'DETECTION_BINARY_THRESHOLD_MAX' : 255,
	        'DETECTION_OFFSET' : 200,

	        'ORIENTATION_BLUR' : (5,5),
	        'ORIENTATION_COLOR_LOW' : 45,
	        'ORIENTATION_COLOR_HIGH': 60,
	        'ORIENTATION_KERNEL' : (100,100),
	        'ORIENTATION_ELEMENT_SIZE_MIN' : 350,
	        'ORIENTATION_ELEMENT_SIZE_MAX' : 600,

	        'ORIENTATION_TEMPLATES' : ['shape_top.png','shape_bottom.png','shape_left.png','shape_right.png']
	        }


	def detectBoard (cameraimage):
		# blur
		IM_blur = cv2.blur(cameraimage,Dartboard_Detector.ENV['DETECTION_BLUR'])

		# convert to HSV (Hue, Saturation, Value: Converted from RGB)
		base_frame_hsv = cv2.cvtColor(IM_blur, cv2.COLOR_BGR2HSV)

		# Extract green areas
		green_thres_low = int(Dartboard_Detector.ENV['DETECTION_GREEN_LOW'] /255. * 180)
		green_thres_high = int(Dartboard_Detector.ENV['DETECTION_GREEN_HIGH'] /255. * 180)
		green_min = np.array([green_thres_low, 100, 100],np.uint8)
		green_max = np.array([green_thres_high, 255, 255],np.uint8)
		frame_threshed_green = cv2.inRange(base_frame_hsv, green_min, green_max)

		#Extract Red
		red_thres_low = int(Dartboard_Detector.ENV['DETECTION_RED_LOW'] /255. * 180)
		red_thres_high = int(Dartboard_Detector.ENV['DETECTION_RED_HIGH'] /255. * 180)
		red_min = np.array([red_thres_low, 100, 100],np.uint8)
		red_max = np.array([red_thres_high, 255, 255],np.uint8)
		frame_threshed_red = cv2.inRange(base_frame_hsv, red_min, red_max)

		#Combine
		combined = frame_threshed_red + frame_threshed_green

		#Close
		kernel = np.ones(Dartboard_Detector.ENV['DETECTION_STRUCTURING_ELEMENT'],np.uint8)
		closing = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel)
		
		#GUI.show(closing, "Dart_Detector")
		#find contours
		ret,thresh = cv2.threshold(combined,Dartboard_Detector.ENV['DETECTION_BINARY_THRESHOLD_MIN'],Dartboard_Detector.ENV['DETECTION_BINARY_THRESHOLD_MAX'],0)
		im2, contours, hierarchy = cv2.findContours(closing.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		max_cont = -1   
		max_idx = 0
		for i in range(len(contours)):
		    length = cv2.arcLength(contours[i], True)
		    if  length > max_cont:
		        max_idx = i
		        max_cont = length
		x,y,w,h = cv2.boundingRect(contours[max_idx])
		x = x-Dartboard_Detector.ENV['DETECTION_OFFSET']
		y = y-Dartboard_Detector.ENV['DETECTION_OFFSET']
		w = w+int(2*Dartboard_Detector.ENV['DETECTION_OFFSET'])
		h = h+int(2*Dartboard_Detector.ENV['DETECTION_OFFSET'])
		return x,y,w,h,closing,frame_threshed_green,frame_threshed_red
