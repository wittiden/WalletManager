from typing import Any, TYPE_CHECKING

from app.core.enums.user_enums import UserStatusesEnum
from app.core.validations.exceptions import UserIsNotAdminError, IsNoneError, IsInstanceError, IsEmptyError, \
    UserIsNotClientError

if TYPE_CHECKING:
    from app.users.domain import UserBase


class GeneralValidation:
    """Класс для общих методов валидации"""

    @staticmethod
    def not_none_checker(value: Any) -> Any:
        if value is None:
            raise IsNoneError(f'{value} is none')

        return value

    @staticmethod
    def not_empty_checker(value: str) -> str:
        if not value:
            raise IsEmptyError(f'{value} is empty')

        return value

    @staticmethod
    def isinstance_checker(value: Any, valid_type: Any) -> Any:
        if not isinstance(value, valid_type):
            raise IsInstanceError(f'{value} must be {valid_type}')

        return value


class UseCasesValidation:
    """Класс для валидации внутри use-cases"""

    @staticmethod
    def is_admin_checker(user: 'UserBase') -> 'UserBase':
        if user.status != UserStatusesEnum.ADMIN:
            raise UserIsNotAdminError(f'{user.status} != Admin')

        return user

    @staticmethod
    def is_client_checker(user: 'UserBase') -> 'UserBase':
        if user.status != UserStatusesEnum.CLIENT:
            raise UserIsNotClientError(f'{user.status} != Client')

        return user