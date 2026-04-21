import sys

from loguru import logger


def add_logger():
    """Функция для настройки логгера"""

    logger.remove()
    logger.add(sys.stdout, level='INFO')
    logger.add('logs/user_logs.log', level='DEBUG', rotation='10 MB')
