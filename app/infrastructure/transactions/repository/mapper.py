from typing import TYPE_CHECKING

from app.common.enums.transaction_enums import TransactionTypesEnum
from app.database.models.transaction import TransactionTable

if TYPE_CHECKING:
    from app.infrastructure.transactions.domain import TransactionBase
    from app.infrastructure.transactions.factory import TransactionFactory


class TransactionMapper:
    """Mapper класс для преобразования transaction->orm_transaction, orm_transaction->transaction"""

    def __init__(self, transaction_factory: 'TransactionFactory') -> None:
        self._transaction_factory = transaction_factory

    def table_to_domain(self, transaction_table: 'TransactionTable') -> 'TransactionBase':
        if transaction_table is None:
            raise ValueError

        if transaction_table.operation_type == TransactionTypesEnum.DEPOSIT or transaction_table.operation_type == TransactionTypesEnum.WITHDRAW:
            obj = self._transaction_factory.create_transaction(
                transaction_table.operation_type,
                transaction_table.from_address,
                transaction_table.to_address,
                transaction_table.completed_at,
                transaction_table.amount,
                transaction_table.fee,
                transaction_table.from_currency,
            )

        elif transaction_table.operation_type == TransactionTypesEnum.EXCHANGE:
            obj = self._transaction_factory.create_transaction(
                transaction_table.operation_type,
                transaction_table.from_address,
                transaction_table.to_address,
                transaction_table.completed_at,
                transaction_table.amount,
                transaction_table.fee,
                transaction_table.from_currency,
                transaction_table.to_currency,
                transaction_table.rate,
            )

        else:
            raise ValueError(f'Unknown status: {transaction_table.operation_type}')

        obj.item_id = transaction_table.transaction_id
        obj.operation_status = transaction_table.operation_status

        return obj

    @staticmethod
    def domain_to_table(transaction: 'TransactionBase') -> 'TransactionTable':
        if transaction.operation_type == TransactionTypesEnum.DEPOSIT or transaction.operation_type == TransactionTypesEnum.WITHDRAW:
            obj = TransactionTable(
                transaction_id=transaction.item_id,
                from_address=transaction.from_address,
                to_address=transaction.to_address,
                completed_at=transaction.completed_at,
                amount=transaction.amount,
                fee=transaction.fee,
                operation_status=transaction.operation_status,
                operation_type=transaction.operation_type,
                from_currency=transaction.currency,
            )

        elif transaction.operation_type == TransactionTypesEnum.EXCHANGE:
            obj = TransactionTable(
                transaction_id=transaction.item_id,
                from_address=transaction.from_address,
                to_address=transaction.to_address,
                completed_at=transaction.completed_at,
                amount=transaction.amount,
                fee=transaction.fee,
                operation_status=transaction.operation_status,
                operation_type=transaction.operation_type,
                from_currency=transaction.from_currency,
                to_currency=transaction.to_currency,
                rate=transaction.rate,
            )

        else:
            raise ValueError(f'Unknown status: {transaction.operation_type}')

        return obj
