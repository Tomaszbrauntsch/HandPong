# import cv2
# import numpy as np
#
# lowerBound = np.array([33,80,40])
# upperBound = np.array([102,255,255])
# cam = cv2.VideoCapture(0)
# ont = cv2.FONT_HERSHEY_SIMPLEX
#
# while(True):
#     ret, img = cam.read()
#     img = cv2.resize(img,(340,240))
#     imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#     mask = cv2.inRange(imgHSV,lowerBound,upperBound)
#     cv2.imshow("mask",mask)
#     cv2.imshow("cam",img)
#
#     kernelOpen = np.ones((5,5))
#     kernelClose = np.ones((20,20))
#
#     maskOpen = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
#     maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_OPEN,kernelClose)
#     cv2.imshow("maskClose", maskClose)
#     cv2.imshow("maskOpen", maskOpen)
#
#     maskFinal=maskClose
#     const
#
#     cv2.waitKey(10)
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()

    #operations here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #display frame from operation above
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) && 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
