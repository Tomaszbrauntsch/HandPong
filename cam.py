import numpy as np
import cv2

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    #operations here
    lower_orange = np.array([12,222,199])
    upper_orange = np.array([180,255,232])
    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv.inRange(HSV, lower_orange, upper_orange)

    res = cv.bitwise_and(frame,frame, mask=mask)
    #display frame from operation above
    cv2.imshow('frame', HSV)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
