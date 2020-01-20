import sys
import numpy as np
import cv2

blue = sys.argv[1] #looks at first argument in commandline inputed
green = sys.argv[2] #looks at second argument in commandline inputed
red = sys.argv[3] #looks at third argument in commandline inputed

color = np.uint8([[[blue,green,red]]])
hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
hue = hsv_color[0][0][0]

print("Lower Bound is")
print("[" + str(hue-10) + ", 100, 100]\n")

print("Upper bound is :"),
print("[" + str(hue + 10) + ", 255, 255]")
