from typing import TYPE_CHECKING

from app.database.models.user import UserTable

if TYPE_CHECKING:
    from app.infrastructure.users.domain import UserBase
    from app.infrastructure.users.factory import UserFactory


class UserMapper:
    """Mapper класс для преобразования user->orm_user, orm_user->user"""

    def __init__(self, user_factory: 'UserFactory') -> None:
        self._user_factory = user_factory

    @staticmethod
    def domain_to_table(user: 'UserBase') -> 'UserTable':
        return UserTable(user_id=user.item_id, name=user.name, email=user.email, password=user.password, is_blocked=user.is_blocked, status=user.status)

    def table_to_domain(self, user_table: 'UserTable') -> 'UserBase':
        obj = self._user_factory.create_user(user_table.status, user_table.name, user_table.email, user_table.password, user_table.is_blocked)
        obj.item_id = user_table.user_id
        return obj