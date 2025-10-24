import cv2
import numpy as np
import mss
import pytesseract
from PIL import Image
from loguru import logger

class ScreenDetector:
    '''Screen detection untuk game analysis'''
    
    def __init__(self, config):
        self.config = config
        self.sct = mss.mss()
        
        # Set tesseract path
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        logger.info('Screen Detector initialized')
    
    def capture_screen(self, region=None):
        '''Capture screenshot'''
        if region:
            monitor = {
                'top': region[1],
                'left': region[0],
                'width': region[2] - region[0],
                'height': region[3] - region[1]
            }
        else:
            monitor = self.sct.monitors[1]
        
        screenshot = self.sct.grab(monitor)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    def detect_hp_percentage(self):
        '''Detect HP bar percentage'''
        hp_region = self.config['detection']['hp_bar_position']
        screenshot = self.capture_screen(hp_region)
        
        # Convert to HSV for color detection
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        
        # Detect red color (HP bar)
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        
        # Calculate percentage
        total_pixels = mask.shape[0] * mask.shape[1]
        red_pixels = np.sum(mask > 0)
        percentage = (red_pixels / total_pixels) * 100
        
        return percentage
    
    def detect_mp_percentage(self):
        '''Detect MP bar percentage'''
        mp_region = self.config['detection']['mp_bar_position']
        screenshot = self.capture_screen(mp_region)
        
        # Convert to HSV
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        
        # Detect blue color (MP bar)
        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # Calculate percentage
        total_pixels = mask.shape[0] * mask.shape[1]
        blue_pixels = np.sum(mask > 0)
        percentage = (blue_pixels / total_pixels) * 100
        
        return percentage
    
    def detect_monster(self):
        '''Detect monster on screen'''
        screenshot = self.capture_screen()
        
        # Convert to HSV
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        
        # Detect monster color
        monster_color = self.config['detection']['monster_color']
        lower = np.array([max(0, monster_color[0]-10), 100, 100])
        upper = np.array([min(255, monster_color[0]+10), 255, 255])
        
        mask = cv2.inRange(hsv, lower, upper)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get largest contour
            largest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest)
            return True, (x + w//2, y + h//2)
        
        return False, None
    
    def find_loot(self):
        '''Find loot items on screen'''
        screenshot = self.capture_screen()
        
        # Detect bright/gold colored items
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        
        lower_gold = np.array([20, 100, 100])
        upper_gold = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_gold, upper_gold)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        loot_positions = []
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Filter small noise
                x, y, w, h = cv2.boundingRect(contour)
                loot_positions.append((x + w//2, y + h//2))
        
        return loot_positions
