from datetime import datetime
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING

from app.common.enums.transaction_enums import TransactionStatusesEnum
from app.common.enums.transaction_enums import TransactionTypesEnum
from app.core.validations import GeneralValidation
from app.core.decorators import debug_log, info_log

if TYPE_CHECKING:
    from app.infrastructure.transactions.repository.commands import TransactionCommandsRepository
    from app.infrastructure.transactions.repository.queries import TransactionQueriesRepository
    from app.infrastructure.transactions.domain import TransactionBase
    from app.infrastructure.transactions.factory import TransactionFactory
    from app.infrastructure.transactions.schemas import CreateDepositTransactionSchema, CreateExchangeTransactionSchema, \
        CreateWithdrawTransactionSchema


class TransactionServiceFacade:
    """Фасад класс для создания общего интерфейса работы с сервисами транзакций"""

    def __init__(self, transaction_create_service: 'CreateTransactionService', transaction_show_service: 'ShowTransactionService', transaction_sort_service: 'SortTransactionService') -> None:
        self._transaction_create_service = transaction_create_service
        self._transaction_show_service = transaction_show_service
        self._transaction_sort_service = transaction_sort_service

    @debug_log
    @info_log(strat_info=None, end_info='Транзакция создана')
    def create_transaction(self, schema: 'CreateDepositTransactionSchema | CreateWithdrawTransactionSchema | CreateExchangeTransactionSchema'):
        if schema.operation_type == TransactionTypesEnum.DEPOSIT:
            obj = self._transaction_create_service.create_deposit_transaction(schema.operation_type, schema.from_address, schema.to_address, schema.amount, schema.operation_status)
        elif schema.operation_type == TransactionTypesEnum.WITHDRAW:
            obj = self._transaction_create_service.create_withdraw_transaction(schema.operation_type, schema.from_address, schema.to_address, schema.amount, schema.operation_status, schema.withdraw_fee)
        elif schema.operation_type == TransactionTypesEnum.EXCHANGE:
            obj = self._transaction_create_service.create_exchange_transaction(schema.operation_type, schema.from_address, schema.to_address, schema.amount, schema.operation_status, schema.exchange_fee, schema.from_currency, schema.to_currency)
        else:
            raise ValueError(f"Unknown type: {schema.operation_type}")

        return obj

    @debug_log
    @info_log(strat_info='Информация о транзакции:', end_info=None)
    def show_transaction(self, find_transaction_id: str) -> 'TransactionBase':
        return self._transaction_show_service.show_transaction(find_transaction_id)

    @debug_log
    @info_log(strat_info='Информация о транзакциях:', end_info=None)
    def show_all_transactions(self) -> list['TransactionBase']:
        return self._transaction_show_service.show_all_transactions()

    @debug_log
    @info_log(strat_info='Отсортированная информация о транзакциях:', end_info=None)
    def sort_all_transactions(self, order_by_param: str) -> list['TransactionBase']:
        return self._transaction_sort_service.sort_all_transactions(order_by_param)


class CreateTransactionService:
    """Сервис класс для создания транзакции"""

    def __init__(self, transaction_factory: 'TransactionFactory', transaction_commands_repository: 'TransactionCommandsRepository') -> None:
        self._transaction_factory = transaction_factory
        self._transaction_commands_repository = transaction_commands_repository

    def create_deposit_transaction(self, key: 'TransactionTypesEnum', from_address: str, to_address: str,  amount: Decimal, operation_status: 'TransactionStatusesEnum') -> 'TransactionBase':
        completed_at = datetime.now()
        transaction = self._transaction_factory.create_transaction(key, from_address, to_address, completed_at, amount, operation_status)
        GeneralValidation.not_none_checker(transaction)

        try:
            self._transaction_commands_repository.insert_transaction_info(transaction)
        except IntegrityError:
            raise

        return transaction

    def create_withdraw_transaction(self, key: 'TransactionTypesEnum', from_address: str, to_address: str,  amount: Decimal, operation_status: 'TransactionStatusesEnum', withdraw_fee: Decimal):
        if from_address != to_address:
            raise ValueError

        completed_at = datetime.now()
        transaction = self._transaction_factory.create_transaction(key, from_address, to_address, completed_at, amount, operation_status, withdraw_fee)
        GeneralValidation.not_none_checker(transaction)

        try:
            self._transaction_commands_repository.insert_transaction_info(transaction)
        except IntegrityError:
            raise

        return transaction

    def create_exchange_transaction(self, key: 'TransactionTypesEnum', from_address: str, to_address: str,  amount: Decimal, operation_status: 'TransactionStatusesEnum', exchange_fee: Decimal, from_currency: str, to_currency: str):
        if from_currency == to_currency:
            raise ValueError

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