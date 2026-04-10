from typing import TYPE_CHECKING

from app.core.validations.exceptions import ElementNotFoundError
from app.core.validations.general_validations import GeneralValidation

if TYPE_CHECKING:
    from app.transactions.domain import TransactionBase


class TransactionRepository:
    """Класс репозиторий для хранения транзакций"""

    def __init__(self) -> None:
        self._transactions: dict[str, 'TransactionBase'] = {}

    def get_transaction(self, transaction_id: str) -> 'TransactionBase':
        return GeneralValidation.not_none_checker(self._transactions.get(transaction_id))

    def get_all_transactions(self) -> list['TransactionBase']:
        return list(self._transactions.values())

    def add_transaction(self, transaction: 'TransactionBase') -> None:
        self._transactions[transaction.item_id] = transaction

    def del_transaction(self, transaction_id: str) -> None:
        if not transaction_id in self._transactions:
            raise ElementNotFoundError(f'transaction #{transaction_id} not found')

        del self._transactions[transaction_id]