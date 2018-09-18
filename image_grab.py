# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 18:26:07 2018

@author: Minh
"""
import time
import cv2
import mss
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from send_input import PressKey, ReleaseKey, UP, DOWN, LEFT, RIGHT, BRAKE, NITROUS

lower_yellow = np.array([20, 30, 30])
upper_yellow = np.array([40, 255, 255])
lower_white = np.array([0, 0, 100])
upper_white = np.array([255, 50, 255])

roi_vertices = [(0, 600), (400, 300), (800, 600)]

def region_of_interest(img, vertices):
    # Define a blank matrix that matches the image height/width.
    mask = np.zeros_like(img)
    # Retrieve the number of color channels of the image.
    #channel_count = img.shape[2]
    # Create a match color with the same color channel counts.
    match_mask_color = (255,) * 4
      
    # Fill inside the polygon
    cv2.fillPoly(mask, vertices, match_mask_color)
    
    # Returning the image only where mask pixels match
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def lane_detection(original_image):
    #gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    #detecting yellow lines
    #blurred_image = cv2.GaussianBlur(original_image, (15,15), 5)
    hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    white_mask = cv2.inRange(hsv_image, lower_white, upper_white)
    #mask of both gray and yellow
    #blurred_yellow = cv2.GaussianBlur(yellow_mask, (15, 15), 0)
    #blurred_white = cv2.GaussianBlur(white_mask, (15, 15), 0)
    mask_yw = cv2.bitwise_or(yellow_mask, white_mask)
    #blurring the image to remove noise
    blurred_image = cv2.GaussianBlur(mask_yw, (9,9), 0)
    #blurred_image = cv2.medianBlur(mask_yw, 7)
    #blurred_image = cv2.bilateralFilter(mask_yw, 15, 150, 150)
    #canny edge detection
    canny_image = cv2.Canny(blurred_image, 120, 150)
    #cropped_image = region_of_interest(canny_image, np.array([roi_vertices], np.int32))
    return canny_image

for i in range(4):
    print(i+1)
    time.sleep(1)

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 0, "left": 0, "width": 800, "height": 600}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))
        canny_image = lane_detection(img)
        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", canny_image)
        print("fps: {0}".format(1 / (time.time() - last_time)))
        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break