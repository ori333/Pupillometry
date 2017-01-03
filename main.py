import numpy as np
import cv2  #add OpenCV Library
import argparse
import math
import matplotlib.pyplot as plt

img = cv2.imread('test.png',0)
imgColor = cv2.imread('test.png',1)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100, circles=2, param1=50,param2=40,minRadius=100,maxRadius=150)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)


#Find contour
imgray = cv2.cvtColor(imgColor,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,65,255,0)
#cv2.imshow('threshold',thresh)

#find the iris contour
#4 for this image
_, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imgColor, contours, 4, (0,255,0), 3)
cv2.circle(imgColor,(i[0],i[1]),2,(0,0,255),3)

#print contours[4]

#Find distance from center of circle and contour
Csize, _ , _ = contours[4].shape
radius = np.empty(Csize)
index = 0
for n in contours[4]:
	dx = i[0]-n[0][0]
	dy = i[1]-n[0][1]
	radius[index] = math.sqrt( dx**2 + dy**2 )
	index += 1


#Find angle from center of circle and contour
rads = np.empty(Csize)
index = 0
for n in contours[4]:
	dx = i[0]-n[0][0]
	dy = i[1]-n[0][1]
	rads[index] = math.atan2(dy,dx)
	index += 1

#print rads


#Countours output array of arrays
cv2.imshow('original image',imgColor)
cv2.imshow('detected circles',cimg)


plt.plot(rads,radius,'ro')
plt.ylabel('radius (pixels)')
plt.xlabel('angle (radians)')
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()

