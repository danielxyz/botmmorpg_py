import time
import threading
from loguru import logger
import keyboard
import pyautogui

class BotEngine:
    '''Core bot engine untuk game automation'''
    
    def __init__(self, config):
        self.config = config
        self.running = False
        self.paused = False
        self.combat_thread = None
        self.heal_thread = None
        
        # Setup pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        logger.info('Bot Engine initialized')
    
    def start(self):
        '''Start bot'''
        if self.running:
            logger.warning('Bot already running')
            return
        
        self.running = True
        logger.info('Bot started')
        
        # Start threads
        self.combat_thread = threading.Thread(target=self._combat_loop, daemon=True)
        self.heal_thread = threading.Thread(target=self._heal_loop, daemon=True)
        
        self.combat_thread.start()
        self.heal_thread.start()
    
    def stop(self):
        '''Stop bot'''
        self.running = False
        logger.info('Bot stopped')
    
    def pause(self):
        '''Pause bot'''
        self.paused = not self.paused
        status = 'paused' if self.paused else 'resumed'
        logger.info(f'Bot {status}')
    
    def _combat_loop(self):
        '''Main combat loop'''
        while self.running:
            if self.paused:
                time.sleep(0.5)
                continue
            
            try:
                # Auto combat logic
                self._attack()
                time.sleep(0.5)
            except Exception as e:
                logger.error(f'Combat error: {e}')
    
    def _heal_loop(self):
        '''Healing loop'''
        while self.running:
            if self.paused:
                time.sleep(0.5)
                continue
            
            try:
                # Auto heal logic
                self._check_health()
                time.sleep(1)
            except Exception as e:
                logger.error(f'Heal error: {e}')
    
    def _attack(self):
        '''Attack logic'''
        attack_key = self.config['combat']['attack_key']
        pyautogui.press(attack_key)
    
    def _check_health(self):
        '''Check and heal if needed'''
        # Placeholder - akan diimplementasi dengan screen detection
        pass
