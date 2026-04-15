from decimal import Decimal
from typing import TYPE_CHECKING, Any
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.database.models import WalletTable, BalanceTable
from app.wallets.repository.mapper import WalletMapper, BalanceMapper

if TYPE_CHECKING:
    from app.wallets.domain import WalletBase


class WalletCommandsRepository:
    """Класс репозиторий crud операций кошелька"""

    def __init__(self, session_factory: sessionmaker, wallet_mapper: 'WalletMapper') -> None:
        self._session_factory = session_factory
        self._wallet_mapper = wallet_mapper

    def insert_wallet_info(self, wallet: 'WalletBase') -> None:
        with self._session_factory() as session:
            session.add(self._wallet_mapper.domain_to_table(wallet))
            session.add_all(BalanceMapper.domain_to_table(wallet))
            session.commit()

    def update_wallet_info(self, wallet: 'WalletBase', new_wallet_data: dict[str, Any]) -> None:
        with self._session_factory() as session:
            obj = session.get(WalletTable, wallet.item_id)
            if obj:
                for key, value in new_wallet_data.items():
                    setattr(obj, key, value)

                session.commit()

    def update_balance_info(self, wallet: 'WalletBase', new_balance_data: dict[str, Decimal]) -> None:
            with self._session_factory() as session:
                objs = session.execute(select(BalanceTable).where(BalanceTable.wallet_id == wallet.item_id)).scalars().all()
                if objs is not None:
                    for obj in objs:
                        if obj.balance_currency.name in new_balance_data:
                            obj.balance_amount = new_balance_data[obj.balance_currency.name]

                    session.commit()

    def delete_wallet_info(self, wallet: 'WalletBase') -> None:
        with self._session_factory() as session:
            wallet_obj = session.get(WalletTable, wallet.item_id)
            if wallet_obj:
                session.delete(wallet_obj)

            session.commit()