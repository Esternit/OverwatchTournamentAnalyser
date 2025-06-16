import logging
from pathlib import Path
from data.config import config

class Logger:
    def __init__(self, name=__name__):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(config.LOG_DIR / "parser.log", encoding='utf-8')
            ]
        )
        
        self.logger = logging.getLogger(name)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message, exc_info=True)
    
    def debug(self, message):
        self.logger.debug(message)