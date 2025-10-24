import time
import yaml
import keyboard
from loguru import logger
from bot.detection.screen import ScreenDetector
from bot.actions.player import PlayerActions

class GameBot:
    '''Main game bot controller'''
    
    def __init__(self, config_path='config/config.yaml'):
        # Load config
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.detector = ScreenDetector(self.config)
        self.player = PlayerActions(self.config)
        
        self.running = False
        self.paused = False
        
        # Setup hotkeys
        self._setup_hotkeys()
        
        logger.info('Game Bot initialized')
    
    def _setup_hotkeys(self):
        '''Setup keyboard hotkeys'''
        hotkeys = self.config['hotkeys']
        
        keyboard.add_hotkey(hotkeys['start_bot'], self.start)
        keyboard.add_hotkey(hotkeys['stop_bot'], self.stop)
        keyboard.add_hotkey(hotkeys['emergency_stop'], self.emergency_stop)
        
        logger.info('Hotkeys registered')
    
    def start(self):
        '''Start bot'''
        if self.running:
            logger.warning('Bot already running')
            return
        
        self.running = True
        self.paused = False
        logger.info('🚀 Bot started!')
        
        self.main_loop()
    
    def stop(self):
        '''Stop bot'''
        self.running = False
        logger.info('⏹️ Bot stopped')
    
    def emergency_stop(self):
        '''Emergency stop'''
        self.running = False
        logger.critical('🛑 EMERGENCY STOP!')
    
    def main_loop(self):
        '''Main bot loop'''
        idle_counter = 0
        max_idle = self.config['safety']['idle_timeout']
        
        while self.running:
            try:
                # Check HP
                if self.config['bot_settings']['auto_heal']:
                    hp = self.detector.detect_hp_percentage()
                    hp_threshold = self.config['healing']['hp_threshold']
                    
                    if hp < hp_threshold:
                        self.player.heal_hp()
                        time.sleep(1)
                
                # Check MP
                if self.config['bot_settings']['auto_heal']:
                    mp = self.detector.detect_mp_percentage()
                    mp_threshold = self.config['healing']['mp_threshold']
                    
                    if mp < mp_threshold:
                        self.player.heal_mp()
                        time.sleep(1)
                
                # Detect and attack monster
                if self.config['bot_settings']['auto_combat']:
                    found_monster, monster_pos = self.detector.detect_monster()
                    
                    if found_monster:
                        # Move to monster
                        self.player.move_to(*monster_pos)
                        time.sleep(0.5)
                        
                        # Attack
                        self.player.attack()
                        
                        # Use skills
                        if self.config['bot_settings']['auto_skill']:
                            self.player.skill_rotation()
                        
                        idle_counter = 0
                    else:
                        idle_counter += 1
                
                # Auto loot
                if self.config['bot_settings']['auto_loot']:
                    loot_positions = self.detector.find_loot()
                    
                    if loot_positions:
                        for loot_pos in loot_positions[:3]:  # Max 3 items
                            self.player.move_to(*loot_pos)
                            time.sleep(0.3)
                            self.player.loot_item()
                
                # Anti-detection: random movement
                if self.config['safety']['random_movement']:
                    if idle_counter > 10:
                        self.player.random_movement()
                        idle_counter = 0
                
                # Safety: stop if idle too long
                if idle_counter > max_idle:
                    logger.warning('Idle timeout reached, stopping bot')
                    self.stop()
                
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f'Error in main loop: {e}')
                time.sleep(1)
        
        logger.info('Bot loop ended')
