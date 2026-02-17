import logging
import sys

# Nuevo nivel numérico (entre INFO y WARNING)
SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

def success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)

logging.Logger.success = success

class ColorFormatter(logging.Formatter):
    # Colores ANSI
    green = "\x1b[32;20m"
    cyan = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    reset = "\x1b[0m"
    
    format_str = "[%(asctime)s] [%(levelname)s]: %(message)s"

    FORMATS = {
        logging.INFO: cyan + format_str + reset,
        SUCCESS_LEVEL_NUM: green + format_str + reset, 
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: red + format_str + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.cyan + self.format_str + self.reset)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColorFormatter())
        logger.addHandler(handler)
