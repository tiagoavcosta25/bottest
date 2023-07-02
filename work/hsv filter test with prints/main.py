import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
from screen import Screen

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
#wincap = WindowCapture('Albion Online Client')
# initialize the Vision class
vision_limestone = Vision('metin_processed.jpg')
# initialize the trackbar window
vision_limestone.init_control_gui()

# limestone HSV filter
hsv_filter = HsvFilter(111, 95, 148, 131, 155, 255, 66, 0, 102, 0)

loop_time = time()
while(True):

    # get an updated image of the game
    #screenshot = wincap.get_screenshot()
    screenshot, screenshot_path = Screen.get_screenshot()

    if screenshot is None:
        continue

    # pre-process the image
    processed_image = vision_limestone.apply_hsv_filter(screenshot, None)
    #rocessed_image = vision_limestone.apply_hsv_filter(screenshot, hsv_filter)

    # do object detection
    rectangles = vision_limestone.find(processed_image, 0.89)

    # draw the detection results onto the original image
    output_image = vision_limestone.draw_rectangles(screenshot, rectangles)

    # display the processed image
    cv.imshow('Processed', processed_image)
    #cv.imshow('Matches', output_image)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')