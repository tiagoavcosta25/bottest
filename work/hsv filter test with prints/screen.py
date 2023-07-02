import cv2 as cv
import os
import logging
from PIL import Image

# Change the working directory to the folder this script is in.
screenshots_folder = 'c:/Users/tiago/Desktop/work/hsv filter test with prints/images'
os.chdir(screenshots_folder)

class Screen:

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
            os.remove(screenshot_path)

        if screenshots:
            # Read the latest screenshot.
            latest_screenshot = screenshots[-1]
            screenshot_path = os.path.join(screenshots_folder, latest_screenshot)

            try:
                if not Screen.verify_image(screenshot_path):
                    return None, None

                screenshot = cv.imread(screenshot_path)

                if screenshot is not None:
                    return screenshot, screenshot_path
            except Exception as e:
                print(f"Error loading image: {e}")

        return None, None
            
    @staticmethod
    def delete_screenshot(screenshot_path):
        os.remove(screenshot_path)

    @staticmethod
    def verify_image(file_path):
        try:
            img = Image.open(file_path)
            img.verify()
            return True
        except (IOError, SyntaxError) as e:
            return False