from datetime import datetime
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING, Any

from app.common.enums.transaction_enums import TransactionTypesEnum
from app.core.validations import GeneralValidation
from app.core.decorators import debug_log, info_log

if TYPE_CHECKING:
    from app.infrastructure.transactions.repository.commands import TransactionCommandsRepository
    from app.infrastructure.transactions.repository.queries import TransactionQueriesRepository
    from app.infrastructure.transactions.domain import TransactionBase
    from app.infrastructure.transactions.factory import TransactionFactory
    from app.infrastructure.transactions.schemas import CreateDepositOrWithdrawTransactionSchema, CreateExchangeTransactionSchema

class TransactionServiceFacade:
    """Фасад класс для создания общего интерфейса работы с сервисами транзакций"""

    def __init__(self, transaction_create_service: 'CreateTransactionService', transaction_show_service: 'ShowTransactionService', sort_transaction_service: 'SortTransactionService', update_transaction_service: 'UpdateTransactionService') -> None:
        self._transaction_create_service = transaction_create_service
        self._transaction_show_service = transaction_show_service
        self._sort_transaction_service = sort_transaction_service
        self._update_transaction_service = update_transaction_service

    @debug_log
    @info_log(strat_info=None, end_info='Транзакция создана')
    def create_transaction(self, schema: 'CreateDepositOrWithdrawTransactionSchema | CreateExchangeTransactionSchema'):
        if schema.operation_type == TransactionTypesEnum.DEPOSIT or schema.operation_type == TransactionTypesEnum.WITHDRAW:
            obj = self._transaction_create_service.create_deposit_transaction(schema.operation_type, schema.from_address, schema.to_address, schema.amount, schema.fee, schema.currency)
        elif schema.operation_type == TransactionTypesEnum.EXCHANGE:
            obj = self._transaction_create_service.create_exchange_transaction(schema.operation_type, schema.from_address, schema.to_address, schema.amount, schema.fee, schema.from_currency, schema.to_currency, schema.rate)
        else:
            raise ValueError(f"Unknown type: {schema.operation_type}")

        return obj

    @debug_log
    @info_log(strat_info=None, end_info='Статус транзакции обновлен')
    def update_transaction_status(self, transaction: 'TransactionBase', new_transaction_param: Any) -> None:
        self._update_transaction_service.update_transaction_status(transaction, new_transaction_param)

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
        return self._sort_transaction_service.sort_all_transactions(order_by_param)


class CreateTransactionService:
    """Сервис класс для создания транзакции"""

    def __init__(self, transaction_factory: 'TransactionFactory', transaction_commands_repository: 'TransactionCommandsRepository') -> None:
        self._transaction_factory = transaction_factory
        self._transaction_commands_repository = transaction_commands_repository

    def create_deposit_transaction(self, key: 'TransactionTypesEnum', from_address: str, to_address: str,  amount: Decimal, fee: Decimal, currency: str) -> 'TransactionBase':
        completed_at = datetime.now()
        transaction = self._transaction_factory.create_transaction(key, from_address, to_address, completed_at, amount, fee, currency)
        GeneralValidation.not_none_checker(transaction)

        try:
            self._transaction_commands_repository.insert_transaction_info(transaction)
        except IntegrityError:
            raise

        return transaction

    def create_exchange_transaction(self, key: 'TransactionTypesEnum', from_address: str, to_address: str,  amount: Decimal, fee: Decimal, from_currency: str, to_currency: str, rate: Decimal):
        if from_currency == to_currency:
            raise ValueError

        completed_at = datetime.now()
        transaction = self._transaction_factory.create_transaction(key, from_address, to_address, completed_at, amount, fee, from_currency, to_currency, rate)
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


class UpdateTransactionService:
    """Сервис класс для обновления информации о транзакциях"""

    def __init__(self, transaction_commands_repository: 'TransactionCommandsRepository') -> None:
        self._transaction_commands_repository = transaction_commands_repository

    def update_transaction_status(self, transaction: 'TransactionBase', new_transaction_param: dict[str, Any]) -> None:
        self._transaction_commands_repository.update_transaction_info(transaction, new_transaction_param)