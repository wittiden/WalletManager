from app.common.enums.transaction_enums import TransactionTypesEnum
from app.database.models.transaction import TransactionTable
from app.transactions.domain import TransactionBase, DepositTransaction, WithdrawTransaction, ExchangeTransaction


class TransactionMapper:
    """Mapper класс для преобразования transaction->orm_transaction, orm_transaction->transaction"""

    @staticmethod
    def table_to_domain(transaction_table: 'TransactionTable') -> 'TransactionBase':
        if transaction_table.operation_type == TransactionTypesEnum.DEPOSIT:
            obj = DepositTransaction(_from_address=transaction_table.from_address, _to_address=transaction_table.to_address, _completed_at=transaction_table.completed_at, _amount=transaction_table.amount)

        elif transaction_table.operation_type == TransactionTypesEnum.WITHDRAW:
            obj = WithdrawTransaction(_from_address=transaction_table.from_address, _to_address=transaction_table.to_address, _completed_at=transaction_table.completed_at, _amount=transaction_table.amount, _withdraw_fee=transaction_table.fee)

        elif transaction_table.operation_type == TransactionTypesEnum.EXCHANGE:
            obj = ExchangeTransaction(_from_address=transaction_table.from_address, _to_address=transaction_table.to_address, _completed_at=transaction_table.completed_at, _amount=transaction_table.amount, _exchange_fee=transaction_table.fee, _from_currency=transaction_table.from_currency, _to_currency=transaction_table.to_currency)

        else:
            raise ValueError(f"Unknown status: {transaction_table.operation_type}")

        obj.item_id = transaction_table.transaction_id
        obj.operation_status = transaction_table.operation_status
        return obj

    @staticmethod
    def domain_to_table(transaction: 'TransactionBase') -> 'TransactionTable':
        if transaction.operation_type == TransactionTypesEnum.DEPOSIT:
            obj = TransactionTable(transaction_id=transaction.item_id, from_address=transaction.from_address, to_address=transaction.to_address, completed_at=transaction.completed_at, amount=transaction.amount, operation_status=transaction.operation_status, operation_type=transaction.operation_type)

        elif transaction.operation_type == TransactionTypesEnum.WITHDRAW:
            obj = TransactionTable(transaction_id=transaction.item_id, from_address=transaction.from_address, to_address=transaction.to_address, completed_at=transaction.completed_at, amount=transaction.amount , operation_status=transaction.operation_status, operation_type=transaction.operation_type, fee=transaction.withdraw_fee)

        elif transaction.operation_type == TransactionTypesEnum.EXCHANGE:
            obj = TransactionTable(transaction_id=transaction.item_id, from_address=transaction.from_address, to_address=transaction.to_address, completed_at=transaction.completed_at, amount=transaction.amount , operation_status=transaction.operation_status, operation_type=transaction.operation_type, fee=transaction.exchange_fee, from_currency=transaction.from_currency, to_currency=transaction.to_currency)

        else:
            raise ValueError(f"Unknown status: {transaction.operation_type}")

        return obj