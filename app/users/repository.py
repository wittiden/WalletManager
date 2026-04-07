from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.users.domain import UserBase


class UserRepository:
    """Класс репозиторий для хранения пользователей"""

    def __init__(self) -> None:
        self._users: dict[str, 'UserBase'] = {}

    def add_user(self, user: 'UserBase') -> None:
        self._users[user.item_id] = user

    def get_user(self, key: str) -> 'UserBase':
        return self._users.get(key)

    def get_all_users(self) -> list['UserBase']:
        return list(self._users.values())