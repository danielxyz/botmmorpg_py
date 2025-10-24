import pyautogui
import time
import random
from loguru import logger

class PlayerActions:
    '''Player actions untuk game control'''
    
    def __init__(self, config):
        self.config = config
        self.last_skill_time = {}
        
    def attack(self):
        '''Perform basic attack'''
        attack_key = self.config['combat']['attack_key']
        pyautogui.press(attack_key)
        logger.debug('Attack executed')
    
    def use_skill(self, skill_number):
        '''Use skill'''
        skill_key = self.config['combat'].get(f'skill_{skill_number}')
        if skill_key:
            pyautogui.press(skill_key)
            self.last_skill_time[skill_number] = time.time()
            logger.debug(f'Skill {skill_number} used')
    
    def skill_rotation(self):
        '''Execute skill rotation'''
        delay = self.config['combat']['skill_rotation_delay']
        
        # Check cooldowns and use skills
        for i in range(1, 5):
            last_use = self.last_skill_time.get(i, 0)
            if time.time() - last_use > 5:  # 5 second cooldown
                self.use_skill(i)
                time.sleep(delay)
    
    def heal_hp(self):
        '''Use HP potion'''
        hp_key = self.config['healing']['hp_potion_key']
        pyautogui.press(hp_key)
        logger.info('HP potion used')
    
    def heal_mp(self):
        '''Use MP potion'''
        mp_key = self.config['healing']['mp_potion_key']
        pyautogui.press(mp_key)
        logger.info('MP potion used')
    
    def loot_item(self):
        '''Pickup loot'''
        loot_key = self.config['looting']['loot_key']
        pyautogui.press(loot_key)
        time.sleep(self.config['looting']['loot_delay'])
        logger.debug('Loot picked up')
    
    def move_to(self, x, y):
        '''Move character to position'''
        pyautogui.click(x, y)
        logger.debug(f'Moving to ({x}, {y})')
    
    def random_movement(self):
        '''Random movement untuk anti-detection'''
        screen_width, screen_height = pyautogui.size()
        
        # Random position near center
        center_x, center_y = screen_width // 2, screen_height // 2
        offset = 100
        
        rand_x = center_x + random.randint(-offset, offset)
        rand_y = center_y + random.randint(-offset, offset)
        
        self.move_to(rand_x, rand_y)
        logger.debug('Random movement executed')
