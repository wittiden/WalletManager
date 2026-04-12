from typing import TYPE_CHECKING

from app.core.exceptions import ElementNotFoundError
from app.core.validations import GeneralValidation

if TYPE_CHECKING:
    from app.users.domain import UserBase


class UserRepository:
    """Класс репозиторий для хранения пользователей"""

    def __init__(self) -> None:
        self._users: dict[str, 'UserBase'] = {}

    def get_user(self, user_id: str) -> 'UserBase':
        return GeneralValidation.not_none_checker(self._users.get(user_id))

    def get_all_users(self) -> list['UserBase']:
        return list(self._users.values())

    def add_user(self, user: 'UserBase') -> None:
        self._users[user.item_id] = user

    def del_user(self, user_id: str) -> None:
        if not user_id in self._users:
            raise ElementNotFoundError(f'user #{user_id} not found')

        del self._users[user_id]