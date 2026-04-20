from typing import Any


class DomainInvariant:
    """Класс для проверки инвариантности в доменной логике"""

    @staticmethod
    def no_empty(attrib_name: str, value: str) -> str:
        if not value.strip():
            raise ValueError(f'{attrib_name} is empty')

        return value

    @staticmethod
    def no_empty_collection(attrib_name: str, value: list | dict) -> list | dict:
        if not value:
            raise ValueError(f'{attrib_name} collection is empty')

        return value

    @staticmethod
    def no_none(attrib_name: str, value: Any) -> Any:
        if value is None:
            raise ValueError(f'{attrib_name} is empty')

        return value

    @staticmethod
    def is_instance(attrib_name: str, value: Any, correct_type: type[Any]) -> Any:
        if not isinstance(value, correct_type):
            raise ValueError(f'{attrib_name} must be {correct_type}')

        return value

    @staticmethod
    def no_negative(attrib_name: str, value: Any):
        if value < 0:
            raise ValueError(f'{attrib_name} < 0')

        return value

