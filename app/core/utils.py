import hashlib
from typing import Any

from loguru import logger


def get_hash(obj: Any) -> str:
    """Функция для хэширования методом sha256"""

    return hashlib.sha256(str(obj).encode()).hexdigest()


def blink_func(sender: Any, field: str, old: Any, new: Any):
    logger.debug(f'{type(sender).__name__} #{sender.item_id} | {field}: {old} -> {new}')
