from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.database.models import WalletTable
from app.wallets.repository.mapper import WalletMapper

if TYPE_CHECKING:
    from app.users.domain import UserBase


class WalletQueriesRepository:
    """Класс репозиторий select операций кошелька"""

    def __init__(self, session_factory: sessionmaker, wallet_mapper: 'WalletMapper') -> None:
        self._session_factory = session_factory
        self._wallet_mapper = wallet_mapper

    def select_all_wallets(self):
        with self._session_factory() as session:
            objs = session.execute(select(WalletTable)).scalars().all()
            return [self._wallet_mapper.table_to_domain(obj, obj.balance, obj.owner) for obj in objs]

    def select_my_wallets(self, user: 'UserBase'):
        with self._session_factory() as session:
            objs = session.execute(select(WalletTable).where(WalletTable.owner_id == user.item_id)).scalars().all()
            return [self._wallet_mapper.table_to_domain(obj, obj.balance, obj.owner) for obj in objs]


    def select_wallet(self, find_wallet_id: str):
        with self._session_factory() as session:
            objs = session.execute(select(WalletTable).where(WalletTable.wallet_id == find_wallet_id)).scalars().all()
            return [self._wallet_mapper.table_to_domain(obj, obj.balance, obj.owner) for obj in objs]


    def select_order_by_wallets(self, order_by_param: str):
        with self._session_factory() as session:
            column = getattr(WalletTable, order_by_param)
            objs = session.execute(select(WalletTable).order_by(column)).scalars().all()
            return [self._wallet_mapper.table_to_domain(obj, obj.balance, obj.owner) for obj in objs]

