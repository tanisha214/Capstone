"""
Logger Utility
Centralized logging configuration for the framework
"""
import logging
import os
from utilities.config_reader import ConfigReader


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Returns a configured logger instance.

    Args:
        name (str): Logger name (typically __name__ of calling module)

    Returns:
        logging.Logger: Configured logger
    """
    log_file = ConfigReader.get_log_file()
    log_level_str = ConfigReader.get_log_level()
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)

    # Ensure log directory exists
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(log_level)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # File Handler
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
