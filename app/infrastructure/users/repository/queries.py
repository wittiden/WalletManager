from typing import TYPE_CHECKING
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.database.models import WalletTable
from app.database.models.user import UserTable

if TYPE_CHECKING:
    from app.infrastructure.users.domain import UserBase
    from app.infrastructure.users.repository.mapper import UserMapper
    from app.infrastructure.wallets.repository.mapper import WalletMapper
    from app.infrastructure.wallets.domain import WalletBase


class UserQueriesRepository:
    """Класс репозиторий select операций пользователя"""

    def __init__(self, session_factory: sessionmaker, user_mapper: 'UserMapper', wallet_mapper: 'WalletMapper') -> None:
        self._session_factory = session_factory
        self._user_mapper = user_mapper
        self._wallet_mapper = wallet_mapper

    def select_user_for_email_and_pass(self, email: str, password: str) -> 'UserBase':
        with self._session_factory() as session:
            obj = session.execute(select(UserTable).where(UserTable.email == email, UserTable.password == password)).scalar_one_or_none()

            return self._user_mapper.table_to_domain(obj)

    def select_my_user(self, user: 'UserBase') -> 'UserBase':
        with self._session_factory() as session:
            obj = session.get(UserTable, user.item_id)

            return self._user_mapper.table_to_domain(obj)

    def select_user(self, find_user_id: str) -> 'UserBase':
        with self._session_factory() as session:
            obj = session.execute(select(UserTable).where(UserTable.user_id == find_user_id)).scalar_one_or_none()

            return self._user_mapper.table_to_domain(obj)

    def select_all_users(self) -> list['UserBase']:
        with self._session_factory() as session:
            obj = session.execute(select(UserTable)).scalars().all()

            return [self._user_mapper.table_to_domain(user) for user in obj]

    def select_order_by_users(self, order_by_param: str) -> list['UserBase']:
        with self._session_factory() as session:
            column = getattr(UserTable, order_by_param)
            obj = session.execute(select(UserTable).order_by(column)).scalars().all()

            return [self._user_mapper.table_to_domain(user) for user in obj]

    def select_my_wallets(self, user: 'UserBase') -> list['WalletBase']:
        with self._session_factory() as session:
            objs = session.execute(select(WalletTable).where(WalletTable.owner_id == user.item_id)).scalars().all()
            return [self._wallet_mapper.table_to_domain(obj) for obj in objs]
