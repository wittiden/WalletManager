from typing import TYPE_CHECKING, Any
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete

from app.database.models import BalanceTable

if TYPE_CHECKING:
    from app.infrastructure.balances.domain import ForeignBalance, BalanceBase, RegularBalance
    from app.infrastructure.balances.repository.mapper import BalanceMapper


class BalanceCommandsRepository:
    """Класс репозиторий crud операций баланса"""

    def __init__(self, session_factory: sessionmaker, balance_mapper: 'BalanceMapper') -> None:
        self._session_factory = session_factory
        self._balance_mapper = balance_mapper

    def insert_balance_info(self, balance: 'RegularBalance') -> None:
        with self._session_factory() as session:
            session.add(self._balance_mapper.domain_to_table(balance))
            session.commit()

    def insert_balances_info(self, balance: 'ForeignBalance') -> None:
        with self._session_factory() as session:
            session.add_all(self._balance_mapper.domain_to_tables(balance))
            session.commit()

    def delete_balance_info(self, balance: 'RegularBalance') -> None:
        with self._session_factory() as session:
            session.execute(delete(BalanceTable).where(BalanceTable.wallet_id == balance.wallet_id))
            session.commit()

    def upgrade_balance_info(self, balance: 'BalanceBase', new_balance_params: dict[str, Any]) -> None:
        with self._session_factory() as session:
            objs = session.execute(select(BalanceTable).where(BalanceTable.wallet_id == balance.wallet_id))
            for key, value in new_balance_params:
                for obj in objs:
                    setattr(obj, key, value)

            session.commit()