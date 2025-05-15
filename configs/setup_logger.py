import logging
import sys

class ColoredFormatter(logging.Formatter):
    """Formatter for applying ANSI colors to log messages for console output."""
    COLORS = {
        logging.DEBUG: "\033[0;33m",   # Yellow
        logging.INFO: "\033[0;32m",    # Green
        logging.WARNING: "\033[0;35m", # Purple
        logging.ERROR: "\033[0;31m",   # Red
        logging.CRITICAL: "\033[1;31m" # Bright Red
    }

    def format(self, record):
        formatted_message = super().format(record)

        log_color = self.COLORS.get(record.levelno, "")
        reset_color = "\033[0m"
        return f"{log_color}{formatted_message}{reset_color}"

def setup_logger(name=None, level=logging.INFO, log_to_file=True, file_path="configs/log.log"):
    """
    Set up a logger with:
    - Colored output for the console.
    - Plain text logs for files.

    :param name: Logger name (usually __name__).
    :param level: Logging level (default: logging.INFO).
    :param log_to_file: Default True, log messages are written to `file_path`.
    :param file_path: Path of the log file. Default: "configs/log.log" 
    :return: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if logger.hasHandlers():
        logger.handlers.clear()

    # Console Handler (Colored)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = ColoredFormatter(
        '%(asctime)s [%(levelname)s] %(filename)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File Handler (Plain Text, No Colors)
    if log_to_file:
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(level)
        plain_formatter = logging.Formatter(  # Standard formatter (NO colors)
            '%(asctime)s [%(levelname)s] %(filename)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(plain_formatter)  # Ensure this formatter is applied
        logger.addHandler(file_handler)

    return logger
