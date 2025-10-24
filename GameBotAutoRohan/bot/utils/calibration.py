import cv2
import mss
import numpy as np
from PIL import Image

def calibrate_hp_bar():
    '''Tool untuk calibrate HP bar position'''
    print('Click and drag to select HP bar region')
    print('Press ENTER when done, ESC to cancel')
    
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    # Select ROI
    roi = cv2.selectROI('Select HP Bar', img, False)
    cv2.destroyAllWindows()
    
    if roi[2] > 0 and roi[3] > 0:
        x1, y1, w, h = roi
        x2, y2 = x1 + w, y1 + h
        print(f'HP Bar Position: [{x1}, {y1}, {x2}, {y2}]')
        print('Copy this to config.yaml under detection.hp_bar_position')
        return [x1, y1, x2, y2]
    
    return None

def calibrate_mp_bar():
    '''Tool untuk calibrate MP bar position'''
    print('Click and drag to select MP bar region')
    print('Press ENTER when done, ESC to cancel')
    
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    roi = cv2.selectROI('Select MP Bar', img, False)
    cv2.destroyAllWindows()
    
    if roi[2] > 0 and roi[3] > 0:
        x1, y1, w, h = roi
        x2, y2 = x1 + w, y1 + h
        print(f'MP Bar Position: [{x1}, {y1}, {x2}, {y2}]')
        print('Copy this to config.yaml under detection.mp_bar_position')
        return [x1, y1, x2, y2]
    
    return None

if __name__ == '__main__':
    print('=== Screen Calibration Tool ===')
    print('1. Calibrate HP Bar')
    print('2. Calibrate MP Bar')
    choice = input('Select option: ')
    
    if choice == '1':
        calibrate_hp_bar()
    elif choice == '2':
        calibrate_mp_bar()
