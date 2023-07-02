import cv2 as cv
import numpy as np
from hsvfilter import HsvFilter

class HsvAlgorithm:
    # properties
    processed_needle_img = None
    needle_w = 0
    needle_h = 0
    method = None
    hsv_filter = None

    # constructor
    def __init__(self, processed_needle_img_path, method=cv.TM_CCOEFF_NORMED):
        # load the image we're trying to match
        # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
        self.processed_needle_img = cv.imread(processed_needle_img_path, cv.IMREAD_UNCHANGED)

        # Save the dimensions of the needle image
        self.needle_w = self.processed_needle_img.shape[1]
        self.needle_h = self.processed_needle_img.shape[0]

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

        # North meteor HSV Filter
        self.hsv_filter = HsvFilter(111, 95, 148, 131, 155, 255, 66, 0, 102, 0)

        # Atlantis filter
        #self.hsv_filter = HsvFilter(94, 221, 0, 128,255,255,70,0,86,0)

        # Zung filter, precisa de um melhoramento
        #self.hsv_filter = HsvFilter(0, 251, 0, 12, 255, 198, 148, 0, 0, 30)

        


    def run(self, screenshot, threshold=0.59, max_results=20):
        # pre-process the image
        processed_image = self.apply_hsv_filter(screenshot)

        # run the OpenCV algorithm
        result = cv.matchTemplate(processed_image, self.processed_needle_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        #print(locations)

        # if we found no results, return now. this reshape of the empty array allows us to 
        # concatenate together results without causing an error
        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)

        # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
        # locations by using groupRectangles().
        # First we need to create the list of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        #print(rectangles)

        # for performance reasons, return a limited number of results.
        # these aren't necessarily the best results.
        if len(rectangles) > max_results:
            print('Warning: too many results, raise the threshold.')
            rectangles = rectangles[:max_results]

        return rectangles
    

    # given an image and an HSV filter, apply the filter and return the resulting image.
    def apply_hsv_filter(self, original_image):
        # convert image to HSV
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        # add/subtract saturation and value
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, self.hsv_filter.sAdd)
        s = self.shift_channel(s, -self.hsv_filter.sSub)
        v = self.shift_channel(v, self.hsv_filter.vAdd)
        v = self.shift_channel(v, -self.hsv_filter.vSub)
        hsv = cv.merge([h, s, v])

        # Set minimum and maximum HSV values to display
        lower = np.array([self.hsv_filter.hMin, self.hsv_filter.sMin, self.hsv_filter.vMin])
        upper = np.array([self.hsv_filter.hMax, self.hsv_filter.sMax, self.hsv_filter.vMax])
        # Apply the thresholds
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow() to display it properly
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return img
    
    # apply adjustments to an HSV channel
    # https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c