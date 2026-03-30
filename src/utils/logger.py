import logging
import os

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

   
    if not logger.handlers:
        os.makedirs("reports/logs", exist_ok=True)

        file_handler = logging.FileHandler("reports/logs/test.log", encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
