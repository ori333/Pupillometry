import numpy as np
import cv2  #add OpenCV Library
import argparse
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys, getopt

initThresh = 150 #Initial Threshold Value
pupilMin = 600
pupilMax = 600000

#pupilContour
#input: color image, graysacle theshold, minimum pupil size, maximum pupil size
#output contour
def pupilContour(imgColor,threshold):
	#Find contour
	imgray = cv2.cvtColor(imgColor,cv2.COLOR_BGR2GRAY)
	ret,threshImg = cv2.threshold(imgray,initThresh,255,0)
	cv2.imshow('threshold',threshImg)
	#cv2.imshow('gray',imgray)

	cv2.waitKey(0) #TODO: make this a flag

	#find the iris contour
	#for this image
	_, contours, _ = cv2.findContours(threshImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	lastContour = np.empty(contours[1].shape)
	for contour in contours:
		if cv2.contourArea(contour) > pupilMin and cv2.contourArea(contour) < pupilMax:
			cv2.drawContours(imgColor, contour, -1, (0,255,0), 3)
			lastContour = contour
	return lastContour

#Pupillometry
#input: string of source file
#output: saves CSV file of contour of pupil and avi file
def pupillometry(srcFile):

	cap = cv2.VideoCapture(srcFile)

	# Define the codec and create VideoWriter object
	fourcc = cv2.VideoWriter_fourcc(*'DIVX')
	baseName = os.path.basename(srcFile).split('.')[0]
	out = cv2.VideoWriter(baseName+'_output.avi',fourcc,30,(1920,1080)) #uncompressed

	#CSV file
	# try:
	#     os.remove("data.csv")
	# except:
	#     return "something went wrong"
	csvdata = open(baseName+'.csv', "w")
	csvdata.write('timestamp (ms),data (radius,radians)\n')
	while(cap.isOpened()):
		ret, imgColor = cap.read()
		if ret==True:
			try:
				time = cap.get(cv2.CAP_PROP_POS_MSEC)
				# cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

				for i in xrange(0,20,5):
					try:
						# #Find contour
						lastContour = pupilContour(imgColor,initThresh + i)

						#cv2.imshow('with contours',imgColor)

						#Find distance from center of contour and contour
						Csize, _ , _ = lastContour.shape
						radius = np.empty(Csize)
						M=cv2.moments(lastContour)
						break #exit loop
					except cv2.error as e:
						print('try again')

				index = 0
				centroid_x = int(M['m10']/M['m00'])
				centroid_y = int(M['m01']/M['m00'])
				cv2.circle(imgColor,(centroid_x,centroid_y), 5, (0,0,255), -1)
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

				# # #print rads

				#save to csv
				csvdata.write(str(time)+',')
				np.savetxt(csvdata,radius, '%s',delimiter=',', newline=',')
				csvdata.write('\n')
				csvdata.write(str(time))
				np.savetxt(csvdata, rads, '%s', delimiter=',', newline=',')
				csvdata.write('\n')

				#Countours output array of arrays
				imgray = cv2.cvtColor(imgColor,cv2.COLOR_BGR2GRAY)
				imgColorSmall = cv2.resize(imgColor, (0,0), fx=0.5, fy=0.5)
				imgraySmall = cv2.resize(imgray,(0,0), fx=0.5, fy=0.5)
				cv2.imshow('original image',imgColorSmall)
				cv2.imshow('imgray',imgraySmall)

				out.write(imgColor)

				# plt.ion()
				# plt.clf()
				# plt.axis([-4,4,0,200])
				# plt.plot(rads,radius,'ro')
				# plt.ylabel('radius (pixels)')
				# plt.xlabel('angle (radians)')
				# plt.show()
				# plt.pause(0.10)



				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
			except cv2.error as e:
				print 'error'
		else:
			break

	# Release everything if job is finished
	cap.release()
	out.release
	cv2.destroyAllWindows()

if __name__ == "__main__":

	had_error = False

	print("Welcome to Pupilometry")
	try:
		opts, args = getopt.getopt(sys.argv[1:],"f:") #get filename input
	except getopt.GetoptError as err:
		# print help information and exit:
		print(str(err)) # will print something like "option -a not recognized"
		print("Wrong Usage")
		#usage() TODO: Make usage function
		sys.exit(2)

	for o,a in opts:
		if o == '-f':
			srcFile = a
		else:
			assert False, "unhandled option"
	pupillometry(srcFile)
