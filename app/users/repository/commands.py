from typing import Any, TYPE_CHECKING
from sqlalchemy.orm import sessionmaker

from app.database.models.user import UserTable
from app.users.repository.mapper import UserMapper

if TYPE_CHECKING:
    from app.users.domain import UserBase


class UserCommandsRepository:
    """Класс репозиторий crud операций пользователя"""

    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def insert_user_info(self, user: 'UserBase') -> None:
        with self._session_factory() as session:
            obj = UserMapper.domain_to_table(user)
            session.add(obj)
            session.commit()

    def delete_user_info(self, user: 'UserBase') -> None:
        with self._session_factory() as session:
            obj = session.get(UserTable, user.item_id)
            if obj:
                session.delete(obj)
                session.commit()

    def update_user_info(self, user: 'UserBase', new_user_data: dict[str, Any]) -> None:
        with self._session_factory() as session:
            obj = session.get(UserTable, user.item_id)
            if obj:
                for key, value in new_user_data.items():
                    if value is not None:
                        setattr(obj, key, value)

                session.commit()