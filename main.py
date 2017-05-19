import numpy as np
import cv2  #add OpenCV Library
import argparse
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys

#Add sub directory /Videos

fileDir = os.path.dirname(os.path.realpath('__file__')) #curent file directory
videosDir = fileDir + '\Videos'

#change directory for videos
os.chdir(videosDir)

cap = cv2.VideoCapture('MVI_0077_clipped.mp4')

while(cap.isOpened()):
	ret, imgColor = cap.read()
	if ret==True:
		img = cv2.cvtColor(imgColor,cv2.COLOR_BGR2GRAY)
		img = cv2.medianBlur(img,5)
		cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

		#Find contour
		imgray = cv2.cvtColor(imgColor,cv2.COLOR_BGR2GRAY)
		ret,thresh = cv2.threshold(imgray,40,255,0)
		cv2.imshow('threshold',thresh)


		circles = cv2.HoughCircles(thresh,cv2.HOUGH_GRADIENT,1,100, circles=2, param1=1,param2=10,minRadius=50,maxRadius=140)

		if circles != None:
			circles = np.uint16(np.around(circles))

			for i in circles[0,:]:
			    # draw the outer circle
			    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
			    # draw the center of the circle
			    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

			#find the iris contour
			#4 for this image
			_, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
			lastContour = np.empty(contours[1].shape)
			for contour in contours:
				if cv2.contourArea(contour) > 10000:
					cv2.drawContours(imgColor, contour, -1, (0,255,0), 3)
					lastContour = contour
					# cv2.circle(imgColor,(i[0],i[1]),2,(0,0,255),3)

		#print contour

		#Find distance from center of contour and contour
		Csize, _ , _ = lastContour.shape
		radius = np.empty(Csize)
		index = 0
		M=cv2.moments(lastContour)
		centroid_x = int(M['m10']/M['m00'])
		centroid_y = int(M['m01']/M['m00'])
		for n in lastContour:
			dx = centroid_x-n[0][0]
			dy = centroid_y-n[0][1]
			radius[index] = math.sqrt( dx**2 + dy**2 )
			index += 1


		#Find angle from center of circle and contour
		rads = np.empty(Csize)
		index = 0
		for n in lastContour:
			dx = centroid_x-n[0][0]
			dy = centroid_y-n[0][1]
			rads[index] = math.atan2(dy,dx)
			index += 1

		# #print rads


		#Countours output array of arrays
		cv2.imshow('original image',imgColor)
		#cv2.imshow('detected circles',cimg)

		plt.ion()
		plt.clf()
		plt.axis([-4,4,0,200])
		plt.plot(rads,radius,'ro')
		plt.ylabel('radius (pixels)')
		plt.xlabel('angle (radians)')
		plt.show()
		plt.pause(0.05)



		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	#else:
		#break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()