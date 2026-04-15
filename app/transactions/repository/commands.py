from typing import Any, TYPE_CHECKING
from sqlalchemy.orm import sessionmaker

from app.database.models.transaction import TransactionTable

if TYPE_CHECKING:
    from app.transactions.domain import TransactionBase
    from app.transactions.repository.mapper import TransactionMapper


class TransactionCommandsRepository:
    """Класс репозиторий crud операций транзакций"""

    def __init__(self, session_factory: sessionmaker, transaction_mapper: 'TransactionMapper') -> None:
        self._session_factory = session_factory
        self._transaction_mapper = transaction_mapper

    def insert_transaction_info(self, transaction: 'TransactionBase') -> None:
        with self._session_factory() as session:
            obj = self._transaction_mapper.domain_to_table(transaction)
            session.add(obj)
            session.commit()

    def delete_transaction_info(self, transaction: 'TransactionBase') -> None:
        with self._session_factory() as session:
            obj = session.get(TransactionTable, transaction.item_id)
            if obj:
                session.delete(obj)
                session.commit()

    def update_transaction_info(self, transaction: 'TransactionBase', new_transaction_params: dict[str, Any]) -> None:
        with self._session_factory() as session:
            obj = session.get(TransactionTable, transaction.item_id)
            if obj:
                for key, value in new_transaction_params.items():
                    if value is not None:
                        setattr(obj, key, value)

                session.commit()