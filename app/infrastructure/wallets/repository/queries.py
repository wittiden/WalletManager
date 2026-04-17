from typing import TYPE_CHECKING
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.database.models import WalletTable, BalanceTable
from app.infrastructure.balances.domain import BalanceBase

if TYPE_CHECKING:
    from app.infrastructure.users.domain import UserBase
    from app.infrastructure.wallets.domain import WalletBase
    from app.infrastructure.wallets.repository.mapper import WalletMapper
    from app.infrastructure.balances.repository.mapper import BalanceMapper


class WalletQueriesRepository:
    """Класс репозиторий select операций кошельков"""

    def __init__(self, session_factory: sessionmaker, wallet_mapper: 'WalletMapper', balance_mapper: 'BalanceMapper') -> None:
        self._session_factory = session_factory
        self._wallet_mapper = wallet_mapper
        self._balance_mapper = balance_mapper

    def select_wallet(self, find_wallet_id: str) -> 'WalletBase':
        with self._session_factory() as session:
            obj = session.get(WalletTable, find_wallet_id)

            if obj:
                return self._wallet_mapper.table_to_domain(obj)
            raise

    def select_all_wallets(self) -> list['WalletBase']:
        with self._session_factory() as session:
            objs = session.execute(select(WalletTable)).scalars().all()

            return [self._wallet_mapper.table_to_domain(obj) for obj in objs]

    def select_order_by_all_wallets(self, order_by_param: str) -> list['WalletBase']:
        with self._session_factory() as session:
            column = getattr(WalletTable, order_by_param)
            objs = session.execute(select(WalletTable).order_by(column)).scalars().all()

            return [self._wallet_mapper.table_to_domain(obj) for obj in objs]

    def select_order_by_my_wallets(self, user: 'UserBase', order_by_param: str) -> list['WalletBase']:
        with self._session_factory() as session:
            column = getattr(WalletTable, order_by_param)
            objs = session.execute(select(WalletTable).where(WalletTable.owner_id == user.item_id).order_by(column)).scalars().all()

            return [self._wallet_mapper.table_to_domain(obj) for obj in objs]

    def select_my_wallet(self, user: 'UserBase', my_wallet_id: str) -> 'WalletBase':
        with self._session_factory() as session:
            obj = session.execute(select(WalletTable).where(WalletTable.owner_id == user.item_id, WalletTable.owner_id == my_wallet_id)).scalars().one_or_none()

            if obj:
                return self._wallet_mapper.table_to_domain(obj)
            raise

    def select_my_wallets(self, user: 'UserBase') -> list['WalletBase']:
        with self._session_factory() as session:
            objs = session.execute(select(WalletTable).where(WalletTable.owner_id == user.item_id)).scalars().all()

            return [self._wallet_mapper.table_to_domain(obj) for obj in objs]

    def select_for_close_wallet(self, user: 'UserBase', pin: str, address: str):
        with self._session_factory() as session:
            obj = session.execute(select(WalletTable).where(WalletTable.owner_id == user.item_id, WalletTable.pin == pin, WalletTable.address == address)).scalars().one_or_none()
            if obj:
                return self._wallet_mapper.table_to_domain(obj)
            raise

    def select_my_balance(self, wallet: 'WalletBase') -> 'BalanceBase':
        with self._session_factory() as session:
            obj = session.execute(select(BalanceTable).where(BalanceTable.wallet_id == wallet.item_id)).one_or_none()
            return self._balance_mapper.table_to_domain(obj)

    def select_my_balances(self, wallet) -> 'BalanceBase':
        with self._session_factory() as session:

            objs = session.execute(select(BalanceTable).where(BalanceTable.wallet_id == wallet.item_id)).scalars().all()

            return self._balance_mapper.tables_to_domain(objs)

    def select_balances(self, wallet_id: str) -> 'BalanceBase':
        with self._session_factory() as session:

            objs = session.execute(select(BalanceTable).where(BalanceTable.wallet_id == wallet_id)).scalars().all()

            return self._balance_mapper.tables_to_domain(objs)
