# app/core/logging.py

from loguru import logger
import sys

def setup_logging():
    # logger.remove()  # Remove default logger
    logger.add(sys.stdout, level="DEBUG", format="<green>{time}</green> | <level>{level}</level> | <cyan>{message}</cyan>")

    # to save logs to a file also
    # logger.add("logs/app.log", rotation="10 MB")

    return logger
