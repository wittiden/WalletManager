from datetime import datetime
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING

from app.common.enums.transaction_enums import TransactionStatusesEnum
from app.common.enums.transaction_enums import TransactionTypesEnum
from app.common.enums.wallet_enums import WalletBalanceCurrenciesEnum
from app.core.validations import GeneralValidation
from app.core.decorators import debug_log, info_log

if TYPE_CHECKING:
    from app.transactions.repository.commands import TransactionCommandsRepository
    from app.transactions.repository.queries import TransactionQueriesRepository
    from app.transactions.domain import TransactionBase
    from app.transactions.factory import TransactionFactory
    from app.transactions.schemas import CreateDebitTransactionSchema, CreateExchangeTransactionSchema, \
        CreateWithdrawTransactionSchema


class TransactionServiceFacade:
    """Фасад класс для создания общего интерфейса работы с сервисами транзакций"""

    def __init__(self, transaction_create_service: 'CreateTransactionService', transaction_show_service: 'ShowTransactionService', transaction_sort_service: 'SortTransactionService') -> None:
        self._transaction_create_service = transaction_create_service
        self._transaction_show_service = transaction_show_service
        self._transaction_sort_service = transaction_sort_service

    @debug_log
    @info_log(['', 'Транзакция создана'])
    def create_transaction(self, key: 'TransactionTypesEnum', schema: 'CreateDebitTransactionSchema | CreateWithdrawTransactionSchema | CreateExchangeTransactionSchema'):
        if isinstance(schema, CreateDebitTransactionSchema):
            obj = self._transaction_create_service.create_debit_transaction(key, schema.from_address, schema.to_address, schema.amount, schema.operation_status)
        elif isinstance(schema, CreateWithdrawTransactionSchema):
            obj = self._transaction_create_service.create_withdraw_transaction(key, schema.from_address, schema.to_address, schema.amount, schema.operation_status, schema.withdraw_fee)
        elif isinstance(schema, CreateExchangeTransactionSchema):
            obj = self._transaction_create_service.create_exchange_transaction(key, schema.from_address, schema.to_address, schema.amount, schema.operation_status, schema.exchange_fee, schema.from_currency, schema.to_currency)
        else:
            raise ValueError(f"Unknown type: {schema.operation_type}")

        return obj

    @debug_log
    @info_log(['Информация о транзакции:', ''])
    def show_transaction(self, find_transaction_id) -> 'TransactionBase':
        return self._transaction_show_service.show_transaction(find_transaction_id)

    @debug_log
    @info_log(['Информация о транзакциях:', ''])
    def show_all_transactions(self) -> list['TransactionBase']:
        return self._transaction_show_service.show_all_transactions()

    @debug_log
    @info_log(['Отсортированные транзакции:', ''])
    def sort_all_transactions(self, order_by_param: str) -> list['TransactionBase']:
        return self._transaction_sort_service.sort_all_transactions(order_by_param)


class CreateTransactionService:
    """Сервис класс для создания транзакции"""

    def __init__(self, transaction_factory: 'TransactionFactory', transaction_commands_repository: 'TransactionCommandsRepository') -> None:
        self._transaction_factory = transaction_factory
        self._transaction_commands_repository = transaction_commands_repository

    def create_debit_transaction(self, key: 'TransactionTypesEnum', from_address: str, to_address: str,  amount: Decimal, operation_status: 'TransactionStatusesEnum') -> 'TransactionBase':
        completed_at = datetime.now()
        transaction = self._transaction_factory.create_transaction(key, from_address, to_address, completed_at, amount, operation_status)
        GeneralValidation.not_none_checker(transaction)

        try:
            self._transaction_commands_repository.insert_transaction_info(transaction)
        except IntegrityError:
            raise

        return transaction

    def create_withdraw_transaction(self, key: 'TransactionTypesEnum', from_address: str, to_address: str,  amount: Decimal, operation_status: 'TransactionStatusesEnum', withdraw_fee: Decimal):
        completed_at = datetime.now()
        transaction = self._transaction_factory.create_transaction(key, from_address, to_address, completed_at, amount, operation_status, withdraw_fee)
        GeneralValidation.not_none_checker(transaction)

        try:
            self._transaction_commands_repository.insert_transaction_info(transaction)
        except IntegrityError:
            raise

        return transaction

    def create_exchange_transaction(self, key: 'TransactionTypesEnum', from_address: str, to_address: str,  amount: Decimal, operation_status: 'TransactionStatusesEnum', exchange_fee: Decimal, from_currency: 'WalletBalanceCurrenciesEnum', to_currency: 'WalletBalanceCurrenciesEnum'):
        completed_at = datetime.now()
        transaction = self._transaction_factory.create_transaction(key, from_address, to_address, completed_at, amount, operation_status, exchange_fee, from_currency, to_currency)
        GeneralValidation.not_none_checker(transaction)

        try:
            self._transaction_commands_repository.insert_transaction_info(transaction)
        except IntegrityError:
            raise

        return transaction


class ShowTransactionService:
    """Сервис класс для вывода информации о транзакциях"""

    def __init__(self, transaction_queries_repository: 'TransactionQueriesRepository') -> None:
        self._transaction_queries_repository = transaction_queries_repository

    def show_transaction(self, find_transaction_id: str) -> 'TransactionBase':
        return GeneralValidation.not_none_checker(self._transaction_queries_repository.select_transaction(find_transaction_id))

    def show_all_transactions(self) -> list['TransactionBase']:
        return self._transaction_queries_repository.select_all_transactions()


class SortTransactionService:
    """Сервис класс для сортировки информации о транзакциях"""

    def __init__(self, transaction_queries_repository: 'TransactionQueriesRepository') -> None:
        self._transaction_queries_repository = transaction_queries_repository

    def sort_all_transactions(self, order_by_param: str) -> list['TransactionBase']:
        return self._transaction_queries_repository.sort_all_transactions(order_by_param)