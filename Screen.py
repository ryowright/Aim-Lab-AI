import cv2
import numpy as np
from mss import mss
from PIL import Image
import time
from math import hypot, floor

# x, y coordinates start from top right of image
# Center of mon is (480, 450)
mon = {'top': 120, 'left': 960, 'width': 960, 'height': 900}
center_x_mon = 480
center_y_mon = 450
# Center of entire is (950, 450)
entire = {'top': 125, 'left': 10, 'width': 1900, 'height': 900}
center_x_entire = 950
center_y_entire = 450

sct = mss()

# GRABS ONE IMAGE
time.sleep(3)
min_dist = 0
min_radius = 0
min_x, min_y, curr = 0, 0, 0

image = sct.grab(entire)
image = np.array(image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 5)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, 
                        param1=100, param2=20, minRadius=30,
                        maxRadius=100)
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")

    for count, (x, y, r) in enumerate(circles):
        cv2.circle(image, (x, y), r, (0, 255, 0), 4)
        print("Circle", count, ":\n", x, "", y) # corresponding x and y coordinates per circle
        #print("distance from center to x:", center_x_entire - x)   # x distance from center
        dist = floor(hypot(center_x_entire - x, center_y_entire - y))
        if (min_dist == 0):
            min_dist = dist
            min_radius = r
            min_x, min_y, curr = x, y, count

        elif (dist < min_dist):
            min_dist = dist
            min_radius = r
            min_x, min_y, curr = x, y, count

    x_travel = center_x_entire - min_x
    y_travel = center_y_entire - min_y
    print("Circle with shortest distance is circle:", curr)
    print("Distance to center:", min_dist)
    print("circle x-position:", min_x)
    print("circle y-position:", min_y, "\n")
    if (min_dist < min_radius):
        print("You are on TARGET")
    elif (x_travel < 0 and y_travel < 0):
        print("Aim RIGHT then DOWN")
    elif (x_travel < 0 and y_travel > 0):
        print("Aim RIGHT then UP")
    elif (x_travel > 0 and y_travel < 0):
        print("Aim LEFT then DOWN")
    elif (x_travel > 0 and y_travel > 0):
        print("Aim LEFT then UP")

cv2.imshow('test', image)
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()