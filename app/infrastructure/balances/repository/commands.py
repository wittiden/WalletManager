from typing import TYPE_CHECKING, Any
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete

from app.common.enums.balance_enums import BalanceTypesEnum
from app.database.models import BalanceTable

if TYPE_CHECKING:
    from app.infrastructure.balances.domain import BalanceBase
    from app.infrastructure.balances.repository.mapper import BalanceMapper


class BalanceCommandsRepository:
    """Класс репозиторий crud операций баланса"""

    def __init__(self, session_factory: sessionmaker, balance_mapper: 'BalanceMapper') -> None:
        self._session_factory = session_factory
        self._balance_mapper = balance_mapper

    def insert_balance_info(self, balance: 'BalanceBase') -> None:
        with self._session_factory() as session:
            if balance.balance_type == BalanceTypesEnum.REGULAR:
                session.add(self._balance_mapper.domain_to_table(balance))
            elif balance.balance_type == BalanceTypesEnum.FOREIGN:
                session.add_all(self._balance_mapper.domain_to_table(balance))
            else:
                raise

            session.commit()

    def delete_balance_info(self, balance: 'BalanceBase') -> None:
        with self._session_factory() as session:
            session.execute(delete(BalanceTable).where(BalanceTable.wallet_id == balance.wallet_id))
            session.commit()

    def upgrade_balance_info(self, balance: 'BalanceBase', new_balance_params: dict[str, Any]) -> None:
        with self._session_factory() as session:
            objs = session.execute(select(BalanceTable).where(BalanceTable.wallet_id == balance.wallet_id)).all()
            for key, value in new_balance_params.items():
                for obj in objs:
                    setattr(obj, key, value)

            session.commit()