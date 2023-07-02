import cv2 as cv
import numpy as np
import os
import pyautogui
import time
from PIL import ImageGrab


# Change the working directory to the folder this script is in.
screenshots_folder = 'c:/Users/tiago/Desktop/work/#4 window capture/images'
os.chdir(screenshots_folder)

while(True):
    # Get the list of screenshots in the folder.
    screenshots = os.listdir(screenshots_folder)

    # Sort the screenshots by their modification time (oldest first).
    screenshots.sort(key=lambda x: os.path.getmtime(x))
    
    if screenshots:
        # Read the latest screenshot.
        latest_screenshot = screenshots[-1]
        screenshot_path = os.path.join(screenshots_folder, latest_screenshot)

        try:
            screenshot = cv.imread(screenshot_path)

            if screenshot is not None:
                # Display the screenshot.
                cv.imshow('Computer Vision', screenshot)
                os.remove(screenshot_path)

            # else:
                # print(f"Failed to read image: {screenshot_path}")
                
                 
        except Exception as e:
            print(f"Error loading image: {e}")


    # press 'q' with the output window focused to exit.
    # waits 1ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')