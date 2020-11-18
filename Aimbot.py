import numpy as np
from numpy import array as nparray
from cv2 import cvtColor, medianBlur, circle, HOUGH_GRADIENT, HoughCircles, COLOR_BGR2GRAY
from mss import mss
from time import sleep
from math import floor, hypot
from pydirectinput import keyDown, keyUp

# x, y coordinates start from top right of image
# Center of entire is (950, 450)
entire = {'top': 125, 'left': 10, 'width': 1900, 'height': 900}
center_x_entire = 950
center_y_entire = 450

sct = mss()

def preprocessAndTarget():
    min_dist = 0
    min_radius = 0
    min_x, min_y = 0, 0
    # Grab and preprocess screen
    image = sct.grab(entire)
    image = nparray(image)
    gray = cvtColor(image, COLOR_BGR2GRAY)
    gray = medianBlur(gray, 5)
    circles = HoughCircles(gray, HOUGH_GRADIENT, 1, 50, 
                            param1=100, param2=20, minRadius=20,
                            maxRadius=100)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        for (x, y, r) in circles:
            circle(image, (x, y), r, (0, 255, 0), 4)
            
            dist = floor(hypot(center_x_entire - x, center_y_entire - y))
            if (min_dist == 0):
                min_dist = dist
                min_radius = floor(r)
                min_x, min_y = x, y

            elif (dist < min_dist):
                min_dist = dist
                min_radius = floor(r)
                min_x, min_y = x, y

    x_travel = center_x_entire - min_x
    y_travel = center_y_entire - min_y

    return x_travel, y_travel, min_dist, min_radius


def main():
    sleep(3)
    x_travel, y_travel, min_dist, min_radius = preprocessAndTarget()

    while True:
        while (x_travel < 0):
            keyDown('right')
            keyUp('right')
            x_travel, y_travel, min_dist, min_radius = preprocessAndTarget()
            #if (abs(x_travel) < min_radius):
             #   keyUp('right')
            if (min_dist < min_radius):
                keyDown('space')
                keyUp('space')

        while (x_travel > 0):
            keyDown('left')
            keyUp('left')
            x_travel, y_travel, min_dist, min_radius = preprocessAndTarget()
            #if (abs(x_travel) < min_radius):
            #    keyUp('left')
            if (min_dist < min_radius):
                keyDown('space')
                keyUp('space')

        while (y_travel < 0):
            keyDown('down')
            keyUp('down')
            x_travel, y_travel, min_dist, min_radius = preprocessAndTarget()
            #if (abs(y_travel) < min_radius):
            #    keyUp('down')
            if (min_dist < min_radius):
                keyDown('space')
                keyUp('space')

        while (y_travel > 0):
            keyDown('up')
            keyUp('up')
            x_travel, y_travel, min_dist, min_radius = preprocessAndTarget()
            #if (abs(y_travel) < min_radius):
            #    keyUp('up')
            if (min_dist < min_radius):
                keyDown('space')
                keyUp('space')

main()

# CALCULATE DISTANCES BETWEEN CIRCLES AND SCREEN CENTER
# 1. Grab x and y distances
# 2. get minimum of distances (target that circle first)
#       - dist = math.hypot(center_x_entire - x, center_y_entire - y)
#       - if (min_dist == 0):   # min_dist initialized at top of program
#       -   min_dist = dist
#       -   min_x = x
#       -   min_y = y
#       - else if (dist < min_dist):
#       -   min_dist = dist
#       -   min_x = x
#       -   min_y = y
# 3. Move analog in current direction until center of screen is within r (radius) of circle
#       - if center_x_entire - min_x is NEGATIVE, move RIGHT
#       - if center_x_entire - min_x is POSITIVE, move LEFT
#       - if center_y_entire - min_y is NEGATIVE, move DOWN
#       - if center_y_entire - min_y is POSITIVE, move UP
#       - once current (min_)dist is less than r (radius)...
# 4. click