from hsvalgorithm import HsvAlgorithm

class Detection:

    # threading properties
    stopped = True
    event = None
    rectangles = []
    # properties
    screenshot = None
    hsv_algorithm = None

    def __init__(self, processed_needle_img_path):
        # load the trained model
        self.hsv_algorithm = HsvAlgorithm(processed_needle_img_path)

    def update(self, screenshot):
        self.screenshot = screenshot
        self.rectangles = self.hsv_algorithm.run(self.screenshot)

    def stop(self):
        self.stopped = True
