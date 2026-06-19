import logging
import logging.handlers
import os
from config import settings

def setup_logger():
    """로깅 설정"""
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level))

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.handlers.RotatingFileHandler(
        "logs/app.log",
        maxBytes=10485760,
        backupCount=10
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
