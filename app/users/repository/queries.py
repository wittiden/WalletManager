from typing import TYPE_CHECKING
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.database.models.user import UserTable
from app.users.repository.mapper import UserMapper

if TYPE_CHECKING:
    from app.users.domain import UserBase


class UserQueriesRepository:
    """Класс репозиторий select операций пользователя"""

    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def select_user_for_login(self, email: str, password: str) -> 'UserBase':
        with self._session_factory() as session:
            obj = session.execute(select(UserTable).where(UserTable.email == email, UserTable.password == password)).scalar_one_or_none()

            return UserMapper.table_to_domain(obj)

    def select_my_user(self, user: 'UserBase') -> 'UserBase':
        with self._session_factory() as session:
            obj = session.get(UserTable, user.item_id)

            return UserMapper.table_to_domain(obj)

    def select_user(self, find_user_id: str) -> 'UserBase':
        with self._session_factory() as session:
            obj = session.execute(select(UserTable).where(UserTable.user_id == find_user_id)).scalar_one_or_none()

            return UserMapper.table_to_domain(obj)

    def select_all_users(self) -> list['UserBase']:
        with self._session_factory() as session:
            obj = session.execute(select(UserTable)).scalars().all()

            return [UserMapper.table_to_domain(user) for user in obj]

    def select_order_by_users(self, order_by_param: str) -> list['UserBase']:
        with self._session_factory() as session:
            column = getattr(UserTable, order_by_param)
            obj = session.execute(select(UserTable).order_by(column)).scalars().all()

            return [UserMapper.table_to_domain(user) for user in obj]