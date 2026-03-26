import logging
import os

# 创建 logs 目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def get_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    logger.propagate = False

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        file_handler = logging.FileHandler(
            os.path.join(LOG_DIR, "app.log"), encoding="utf-8"
        )
        file_handler.setLevel(logging.INFO)

        error_handler = logging.FileHandler(
            os.path.join(LOG_DIR, "error.log"), encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
        )

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(error_handler)

    return logger