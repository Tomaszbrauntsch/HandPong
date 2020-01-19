import cv2
import numpy as np

lowerBound = np.array([33,80,40])
upperBound = np.array([102,255,255])
cam = cv2.VideoCapture(0)
ont = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX,2,0.5,0,3,1)
while(True):
    ret, img = cam.read()
    img = cv2.resize(img,(340,240))
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV,lowerBound,upperBound)
    cv2.imshow("mask",mask)
    cv2.imshow("cam",img)
    cv2.waitkey(10)
