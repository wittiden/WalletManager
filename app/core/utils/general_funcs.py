import hashlib
from typing import Any


def get_hash(obj: Any) -> str:
    """Функция для хэширования методом sha256"""

    return hashlib.sha256(str(obj).encode()).hexdigest()