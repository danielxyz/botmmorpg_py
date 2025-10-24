import customtkinter as ctk
import threading
from loguru import logger
from bot.core.bot import GameBot

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

class BotControlPanel(ctk.CTk):
    '''GUI Control Panel untuk Game Bot'''
    
    def __init__(self):
        super().__init__()
        
        self.title('🎮 Rohan 2 & LordNine Game Bot')
        self.geometry('800x600')
        
        self.bot = None
        self.bot_thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = ctk.CTkLabel(
            self,
            text='🎮 Game Bot Control Panel',
            font=ctk.CTkFont(size=28, weight='bold')
        )
        header.pack(pady=20)
        
        # Game selection
        game_frame = ctk.CTkFrame(self)
        game_frame.pack(fill='x', padx=20, pady=10)
        
        ctk.CTkLabel(
            game_frame,
            text='Select Game:',
            font=ctk.CTkFont(size=14)
        ).pack(side='left', padx=10)
        
        self.game_selector = ctk.CTkSegmentedButton(
            game_frame,
            values=['Rohan 2', 'LordNine']
        )
        self.game_selector.pack(side='left', padx=10)
        self.game_selector.set('Rohan 2')
        
        # Features frame
        features_frame = ctk.CTkFrame(self)
        features_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            features_frame,
            text='Bot Features',
            font=ctk.CTkFont(size=18, weight='bold')
        ).pack(pady=10)
        
        # Feature toggles
        self.auto_combat = ctk.CTkSwitch(
            features_frame,
            text='🗡️ Auto Combat',
            font=ctk.CTkFont(size=14)
        )
        self.auto_combat.pack(pady=5)
        self.auto_combat.select()
        
        self.auto_heal = ctk.CTkSwitch(
            features_frame,
            text='💊 Auto Healing',
            font=ctk.CTkFont(size=14)
        )
        self.auto_heal.pack(pady=5)
        self.auto_heal.select()
        
        self.auto_loot = ctk.CTkSwitch(
            features_frame,
            text='💰 Auto Looting',
            font=ctk.CTkFont(size=14)
        )
        self.auto_loot.pack(pady=5)
        self.auto_loot.select()
        
        self.auto_skill = ctk.CTkSwitch(
            features_frame,
            text='⚡ Auto Skill Rotation',
            font=ctk.CTkFont(size=14)
        )
        self.auto_skill.pack(pady=5)
        self.auto_skill.select()
        
        # Status
        self.status_label = ctk.CTkLabel(
            features_frame,
            text='Status: Stopped',
            font=ctk.CTkFont(size=16),
            text_color='red'
        )
        self.status_label.pack(pady=20)
        
        # Control buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill='x', padx=20, pady=20)
        
        self.start_btn = ctk.CTkButton(
            button_frame,
            text='▶️ Start Bot',
            command=self.start_bot,
            font=ctk.CTkFont(size=16, weight='bold'),
            height=50,
            fg_color='green',
            hover_color='darkgreen'
        )
        self.start_btn.pack(side='left', expand=True, padx=5)
        
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text='⏹️ Stop Bot',
            command=self.stop_bot,
            font=ctk.CTkFont(size=16, weight='bold'),
            height=50,
            fg_color='red',
            hover_color='darkred',
            state='disabled'
        )
        self.stop_btn.pack(side='left', expand=True, padx=5)
        
        # Hotkey info
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        info_text = '''
        ⌨️ Hotkeys:
        F9 - Start Bot | F10 - Stop Bot | F12 - Emergency Stop
        '''
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12)
        ).pack(pady=10)
    
    def start_bot(self):
        '''Start the bot'''
        try:
            # Initialize bot
            self.bot = GameBot()
            
            # Update config from GUI
            self.bot.config['bot_settings']['auto_combat'] = self.auto_combat.get()
            self.bot.config['bot_settings']['auto_heal'] = self.auto_heal.get()
            self.bot.config['bot_settings']['auto_loot'] = self.auto_loot.get()
            self.bot.config['bot_settings']['auto_skill'] = self.auto_skill.get()
            
            # Start bot in thread
            self.bot_thread = threading.Thread(target=self.bot.start, daemon=True)
            self.bot_thread.start()
            
            # Update UI
            self.status_label.configure(text='Status: Running', text_color='green')
            self.start_btn.configure(state='disabled')
            self.stop_btn.configure(state='normal')
            
            logger.info('Bot started from GUI')
            
        except Exception as e:
            logger.error(f'Failed to start bot: {e}')
            self.status_label.configure(text=f'Error: {e}', text_color='red')
    
    def stop_bot(self):
        '''Stop the bot'''
        if self.bot:
            self.bot.stop()
            
            # Update UI
            self.status_label.configure(text='Status: Stopped', text_color='red')
            self.start_btn.configure(state='normal')
            self.stop_btn.configure(state='disabled')
            
            logger.info('Bot stopped from GUI')

if __name__ == '__main__':
    app = BotControlPanel()
    app.mainloop()
