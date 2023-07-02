import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture

# Change the working dir to the folder the script is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

wincap = WindowCapture('League of Legends')

loop_time = time()
while(True):

    screenshot = wincap.get_screenshot()

    cv.imshow('Computer Vision', screenshot)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output windows focused to exit
    # waits 1ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


print('Done.')