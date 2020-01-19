import numpy as np
import cv2

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    #operations here
    #RGB = 255,168,11
    #HSV = 39,96,100
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_range = np.array([7,130,130])
    upper_range = np.array([50,255,255])

    mask = cv2.inRange(hsv, lower_range, upper_range)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts)>0:
        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)) , int(radius), (0,255,255), 2)
            cv2.circle(frame, center, 5, (0,0,255), -1)
    #display frame from operation above
    cv2.imshow('frame', frame)
    cv2.imshow('gray', mask)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
