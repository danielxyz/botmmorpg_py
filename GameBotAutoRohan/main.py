#!/usr/bin/env python3
'''
Game Bot Auto Pilot for Rohan 2 & LordNine
Python 3.14 | Simple & Detailed
'''

import sys
from loguru import logger
from bot.gui.control_panel import BotControlPanel

# Setup logging
logger.remove()
logger.add(
    'logs/bot_{time}.log',
    rotation='1 day',
    retention='7 days',
    level='DEBUG',
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}'
)
logger.add(sys.stdout, level='INFO')

def main():
    '''Main entry point'''
    logger.info('=' * 60)
    logger.info('Game Bot Auto Pilot Started')
    logger.info('Python 3.14 | Rohan 2 & LordNine')
    logger.info('=' * 60)
    
    try:
        # Launch GUI
        app = BotControlPanel()
        app.mainloop()
        
    except KeyboardInterrupt:
        logger.info('Bot terminated by user')
    except Exception as e:
        logger.critical(f'Fatal error: {e}')
    finally:
        logger.info('Bot shutdown complete')

if __name__ == '__main__':
    main()
