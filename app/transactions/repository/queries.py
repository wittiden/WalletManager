from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from typing import TYPE_CHECKING

from app.database.models.transaction import TransactionTable
from app.transactions.repository.mapper import TransactionMapper

if TYPE_CHECKING:
    from app.transactions.domain import TransactionBase


class TransactionQueriesRepository:
    """Класс репозиторий select операций транзакций"""

    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def select_transaction(self, find_transaction_id) -> 'TransactionBase':
        with self._session_factory() as session:
            obj = session.get(TransactionTable, find_transaction_id)
            return TransactionMapper.table_to_domain(obj)

    def select_all_transactions(self) -> list['TransactionBase']:
        with self._session_factory() as session:
            obj = session.execute(select(TransactionTable)).scalars().all()
            return [TransactionMapper.table_to_domain(user) for user in obj]

    def sort_all_transactions(self, order_by_param: str) -> list['TransactionBase']:
        with self._session_factory() as session:
            column = getattr(TransactionTable, order_by_param)
            obj = session.execute(select(TransactionTable).order_by(column)).scalars().all()
            return [TransactionMapper.table_to_domain(user) for user in obj]
