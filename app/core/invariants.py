from typing import Any

from app.core.exceptions import IsEmptyError, IsNoneError, IsInstanceError


class DomainInvariant:
    """Класс для проверки инвариантности в доменной логике"""

    @staticmethod
    def no_empty(attrib_name: str, value: str) -> str:
        if not value.strip():
            raise IsEmptyError(f'{attrib_name} is empty')

        return value

    @staticmethod
    def no_none(attrib_name: str, value: Any) -> Any:
        if value is None:
            raise IsNoneError(f'{attrib_name} is empty')

        return value

    @staticmethod
    def is_instance(attrib_name: str, value: Any, correct_type: type[Any]) -> Any:
        if not isinstance(value, correct_type):
            raise IsInstanceError(f'{attrib_name} must be {correct_type}')

        return value
