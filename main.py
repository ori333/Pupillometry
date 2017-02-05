import numpy as np
import cv2  #add OpenCV Library
import argparse
import math
import matplotlib.pyplot as plt
import os
import sys

#Add sub directory /Videos

fileDir = os.path.dirname(os.path.realpath('__file__')) #curent file directory
videosDir = fileDir + '\Videos'

#change directory for videos
os.chdir(videosDir)

cap = cv2.VideoCapture('IR_eye_video.mp4')

while(cap.isOpened()):
	ret, frame = cap.read()

	cv2.imshow('frame',frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()