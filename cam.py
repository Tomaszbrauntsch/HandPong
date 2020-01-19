import numpy as np
import cv2

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    #operations here
    #RGB = 255,168,11
    #HSV = 39,96,100
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_range = np.array([18,100,100])
    upper_range = np.array([38,255,255])

    mask = cv2.inRange(hsv, lower_range, upper_range)

    #display frame from operation above
    cv2.imshow('frame', HSV)
    cv2.imshow('gray', mask)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
