import cv2 as cv
import os
from windowcapture import WindowCapture
from detection import Detection
from vision import Vision
from datetime import datetime
import time
from new_bot import MetinBot

# Change the working directory to the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

# initialize the WindowCapture class
wincap = WindowCapture('Aeldra.to')
# load the detector
detector = Detection('metin_processed.jpg')
# load an empty Vision class
vision = Vision()
# initialize the bot
#bot = AlbionBot((wincap.offset_x, wincap.offset_y), (wincap.w, wincap.h))
bot = MetinBot((wincap.offset_x, wincap.offset_y), (wincap.w, wincap.h))

wincap.start()
#detector.start()
bot.start()

time.sleep(3)

while(True):
    # Get the latest screenshot
    screenshot = wincap.screenshot

    # if we don't have a screenshot yet, don't run the code below this point yet
    if screenshot is None:
        print('{} -> No screenshot available'.format(datetime.now()))        
        continue

    # give detector the current screenshot to search for objects in
    detector.update(screenshot)

    targets = vision.get_click_points(detector.rectangles)

    bot.update_targets(targets)

    '''
    # update the bot with the data it needs right now
    if bot.state == BotState.INITIALIZING:
        # while bot is waiting to start, go ahead and start giving it some targets to work
        # on right away when it does start
        targets = vision.get_click_points(detector.rectangles)
        bot.update_targets(targets)
    elif bot.state == BotState.SEARCHING:
        # when searching for something to click on next, the bot needs to know what the click
        # points are for the current detection results. it also needs an updated screenshot
        # to verify the hover tooltip once it has moved the mouse to that position
        targets = vision.get_click_points(detector.rectangles)
        bot.update_targets(targets)
        bot.update_screenshot(wincap.screenshot)
    elif bot.state == BotState.MOVING:
        # when moving, we need fresh screenshots to determine when we've stopped moving
        bot.update_screenshot(wincap.screenshot)
    elif bot.state == BotState.MINING:
        # nothing is needed while we wait for the mining to finish
        pass

    '''
    
    if DEBUG:
        # draw the detection results onto the original image
        detection_image = vision.draw_rectangles(screenshot, detector.rectangles)
        # display the images
        cv.imshow('Matches', detection_image)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('q'):
        wincap.stop()
        detector.stop()
        bot.stop()
        cv.destroyAllWindows()
        break

print('Done.')
