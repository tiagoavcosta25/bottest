import pyautogui
import cv2 as cv
from math import sqrt
from time import sleep, time
from threading import Thread, Lock, Event
import subprocess
import autoit
import ctypes
import pydirectinput
import keyboard

class MetinBot:

    # Path to the AutoHotkey executable
    autohotkey_path = r'C:\Program Files\AutoHotkey\v1.1.36.02\AutoHotkeyU64.exe'

    # Path to the AHK script
    script_path = r'C:\Users\tiago\Desktop\work\z_bot\script.ahk'

    event = None
    lock = None

    # constants
    INITIALIZING_SECONDS = 6
    MINING_SECONDS = 14
    MOVEMENT_STOPPED_THRESHOLD = 0.975
    IGNORE_RADIUS = 130
    TOOLTIP_MATCH_THRESHOLD = 0.72

    # properties
    stopped = True
    state = None
    targets = []
    screenshot = None
    timestamp = None
    movement_screenshot = None
    window_offset = (0,0)
    window_w = 0
    window_h = 0
    limestone_tooltip = None
    click_history = []

    def __init__(self, window_offset, window_size):
        self.lock = Lock()
        # for translating window positions into screen positions, it's easier to just
        # get the offsets and window size from WindowCapture rather than passing in 
        # the whole object
        self.window_offset = window_offset
        self.window_w = window_size[0]
        self.window_h = window_size[1]
        self.event = Event()
        self.event.set()

    def clickMetin(self):
        return subprocess.Popen([self.autohotkey_path, self.script_path])

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    
    def click_next_target(self):
        # 1. order targets by distance from center
        # loop:
        #   2. hover over the nearest target
        #   3. confirm that it's limestone via the tooltip
        #   4. if it's not, check the next target
        # endloop
        # 5. if no target was found return false
        # 6. click on the found target and return true
        targets = self.targets_ordered_by_distance(self.targets)

        target_i = 0
        # load up the next target in the list and convert those coordinates
        # that are relative to the game screenshot to a position on our
        # screen
        
        try:
            target_pos = targets[target_i]
        except Exception as e:
            return
        
        if len(self.click_history) > 0 and self.click_history[-1] == target_pos and len(targets) > 1:            
            target_pos = targets[target_i + 1]

        screen_x, screen_y = self.get_screen_position(target_pos)
        print('Moving mouse to x:{} y:{}'.format(screen_x, screen_y))
        # move the mouse
        pydirectinput.moveTo(x=screen_x, y=screen_y)
        

        print('Click on confirmed target at x:{} y:{}'.format(screen_x, screen_y))


        # save this position to the click history
        self.click_history.append(target_pos)
        target_i += 1

    def simulate_left_click(self):
        # Define the INPUT structure
        class INPUT(ctypes.Structure):
            _fields_ = [("type", ctypes.c_ulong),
                        ("union", ctypes.POINTER(ctypes.c_ulong * 3))]

        # Define the required Windows constants
        INPUT_MOUSE = 0x0001
        MOUSEEVENTF_LEFTDOWN = 0x0002
        MOUSEEVENTF_LEFTUP = 0x0004

        # Create the INPUT structure and set the mouse event flags
        input_structure = INPUT()
        input_structure.type = INPUT_MOUSE
        input_structure.union = ctypes.pointer((ctypes.c_ulong * 3)(MOUSEEVENTF_LEFTDOWN, 0, 0))

        # Send the left mouse button down event
        ctypes.windll.user32.SendInput(1, ctypes.byref(input_structure), ctypes.sizeof(input_structure))

        # Wait for a small delay
        sleep(0.1)  # Adjust the delay as needed

        # Update the mouse event flags for the left mouse button up event
        input_structure.union = ctypes.pointer((ctypes.c_ulong * 3)(MOUSEEVENTF_LEFTUP, 0, 0))

        # Send the left mouse button up event
        ctypes.windll.user32.SendInput(1, ctypes.byref(input_structure), ctypes.sizeof(input_structure))

    
    def get_screen_position(self, pos):
        return (pos[0] + self.window_offset[0], pos[1] + self.window_offset[1])

    def targets_ordered_by_distance(self, targets):
        # our character is always in the center of the screen
        my_pos = (self.window_w / 2, self.window_h / 2)
        # searched "python order points by distance from point"
        # simply uses the pythagorean theorem
        # https://stackoverflow.com/a/30636138/4655368
        def pythagorean_distance(pos):
            return sqrt((pos[0] - my_pos[0])**2 + (pos[1] - my_pos[1])**2)
        targets.sort(key=pythagorean_distance)

        # print(my_pos)
        # print(targets)
        # for t in targets:
        #    print(pythagorean_distance(t))

        # ignore targets at are too close to our character (within 130 pixels) to avoid 
        # re-clicking a deposit we just mined
        targets = [t for t in targets if pythagorean_distance(t) > self.IGNORE_RADIUS]

        return targets
    
    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()
        self.event.set()

    def run(self):
        while not self.stopped:
            self.event.wait()
            self.lock.acquire()
            if self.targets:
                self.click_next_target()
            self.lock.release()
            sleep(2)
            self.event.clear()

    def stop(self):
        self.stopped = True



