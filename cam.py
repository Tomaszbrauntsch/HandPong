import cv2
import numpy as np

lowerBound = np.array([33,80,40])
upperBound = np.array([102,255,255])
cam = cv2.VideoCapture(0)
ont = cv2.FONT_HERSHEY_SIMPLEX

while(True):
    ret, img = cam.read()
    img = cv2.resize(img,(340,240))
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV,lowerBound,upperBound)
    cv2.imshow("mask",mask)
    cv2.imshow("cam",img)

    kernelOpen = np.ones((5,5))
    kernelClose = np.ones((20,20))

    maskOpen = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_OPEN,kernelClose)
    cv2.imshow("maskClose", maskClose)
    cv2.imshow("maskOpen", maskOpen)

    cv2.waitKey(10)
