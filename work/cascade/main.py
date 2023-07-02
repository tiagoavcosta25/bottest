import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision
from screen import Screen
from hsvfilter import HsvFilter

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
wincap = WindowCapture('Aeldra.to')

# load the trained model
cascade_limestone = cv.CascadeClassifier('cascade/cascade.xml')

# load an empty Vision class
vision_limestone = Vision(None)

vision_limestone.init_control_gui()

# limestone HSV filter
# antigo hsv_filter = HsvFilter(111, 95, 148, 131, 155, 255, 66, 0, 102, 0)
hsv_filter = HsvFilter(110, 3, 0, 128, 33, 123, 0, 22, 0, 74)
# 110 3 0 128 33 123 0 22 0 74
loop_time = time()
while(True):

    # get an updated image of the game
    screenshot, screenshot_path = Screen.get_screenshot()

    if screenshot is None and screenshot_path is None:
        continue


    # pre-process the image
    #processed_image = vision_limestone.apply_hsv_filter(screenshot, hsv_filter)
    processed_image = vision_limestone.apply_hsv_filter(screenshot, None)

    #cv.imshow('Processed', processed_image)

    # do object detection
    rectangles = cascade_limestone.detectMultiScale(screenshot)

    # draw the detection results onto the original image
    detection_image = vision_limestone.draw_rectangles(screenshot, rectangles)

    # display the processed image
    cv.imshow('Matches', detection_image)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


print('Done.')