import cv2 as cv
import win32gui
from threading import Thread, Lock
import os
from PIL import Image
import subprocess

# Change the working directory to the folder this script is in.
screenshots_folder = r'C:\Users\tiago\Desktop\work\z_bot\images'
os.chdir(screenshots_folder)

# Bandicam path
bandicam_path = r'C:\Program Files\Bandicam\bdcam.exe'  

class WindowCapture:

    # threading properties
    stopped = True
    lock = None
    screenshot = None
    event = None
    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    process = None

    # constructor
    def __init__(self, window_name=None):
        # start bandicam
        self.process = subprocess.Popen(bandicam_path)

        # create a thread lock object
        self.lock = Lock()

        # find the handle for the window we want to capture.

        self.hwnd = win32gui.FindWindow(None, window_name)

        if window_name is None or not self.hwnd:
            raise Exception('Please provide an existing Window name')
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    @staticmethod
    def get_screenshot():
        # Get the list of screenshots in the folder.
        screenshots = os.listdir(screenshots_folder)

        # Sort the screenshots by their modification time (oldest first).
        screenshots.sort(key=lambda x: os.path.getmtime(os.path.join(screenshots_folder, x)))

        # Check if there are at least two screenshots
        if len(screenshots) >= 2:
            # Get the path of the second latest screenshot
            screenshot_path = os.path.join(screenshots_folder, screenshots[-2])
            
            # Delete the second latest screenshot
            try:
                os.remove(screenshot_path)
            except Exception as e:
                pass

        if screenshots:
            # Read the latest screenshot.
            latest_screenshot = screenshots[-1]
            screenshot_path = os.path.join(screenshots_folder, latest_screenshot)

            try:
                if not WindowCapture.verify_image(screenshot_path):
                    return None

                screenshot = cv.imread(screenshot_path)

                if screenshot is not None:
                    return screenshot
            except Exception as e:
                print(f"Error loading image: {e}")

        return None

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

    def verify_image(file_path):
        try:
            img = Image.open(file_path)
            img.verify()
            return True
        except (IOError, SyntaxError) as e:
            return False
    
    # threading methods
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            # get an updated image of the game
            screenshot = None
            while screenshot is None:
                screenshot = WindowCapture.get_screenshot()

            # lock the thread while updating the results
            #self.lock.acquire()
            self.screenshot = screenshot
            #self.lock.release()
