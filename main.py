import numpy as np
import cv2  #add OpenCV Library
import argparse
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


#Find angle and distance from center of circle and contour

#Countours output array of arrays

cv2.imshow('original image',imgColor)
cv2.imshow('detected circles',cimg)

#plt.plot(contours[4])
#plt.ylabel('some numbers')
#plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()

