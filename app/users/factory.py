from typing import TYPE_CHECKING, ParamSpec

from app.core.enums.user_enums import UserStatusesEnum
from app.core.validations.general_validations import GeneralValidation

if TYPE_CHECKING:
    from app.users.domain import UserBase

P = ParamSpec('P')


class UserRegistrations:
    """Класс для регистрации типов пользователей"""

    def __init__(self) -> None:
        self._user_registry_dict: dict['UserStatusesEnum', type['UserBase']] = {}

    def set_registration(self, key: 'UserStatusesEnum', value: type['UserBase']) -> None:
        self._user_registry_dict[key] = value

    def get_registration(self, key: 'UserStatusesEnum') -> type['UserBase']:
        return GeneralValidation.not_none_checker(self._user_registry_dict.get(key))

    def get_all_registrations(self) -> dict['UserStatusesEnum', type['UserBase']]:
        return self._user_registry_dict


class UserFactory:
    """Класс фабрика для создания пользователя любого типа"""

    def __init__(self, user_registry_dict: 'UserRegistrations') -> None:
        self._user_registry_dict = user_registry_dict

    def create_user(self, key: 'UserStatusesEnum', *args: P.args, **kwargs: P.kwargs) -> 'UserBase':
        class_type = self._user_registry_dict.get_registration(key)
        return class_type(*args, **kwargs)