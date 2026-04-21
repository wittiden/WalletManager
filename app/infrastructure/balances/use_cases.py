import datetime
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING

from app.common.enums.balance_enums import BalanceTypesEnum
from app.common.enums.transaction_enums import TransactionStatusesEnum
from app.core.decorators import debug_log, info_log
from app.core.validations import UseCasesValidation, GeneralValidation

if TYPE_CHECKING:
    from app.infrastructure.balances.domain import BalanceBase
    from app.infrastructure.balances.factory import BalanceFactory
    from app.infrastructure.balances.repository.commands import BalanceCommandsRepository
    from app.infrastructure.balances.schemas import CreateForeignBalanceSchema
    from app.infrastructure.balances.schemas import CreateRegularBalanceSchema
    from app.infrastructure.users.domain import UserBase
    from app.infrastructure.wallets.domain import WalletBase
    from app.infrastructure.wallets.repository.queries import WalletQueriesRepository
    from app.infrastructure.transactions.domain import TransactionBase
    from app.infrastructure.transactions.repository.commands import TransactionCommandsRepository


class BalanceServiceFacade:
    """Класс фасад для взаимодействия с балансом"""

    def __init__(self, create_balance_service: 'CreateBalanceService', show_balance_service: 'ShowBalanceService', freeze_balance_service: 'FreezeBalanceService') -> None:
        self._create_balance_service = create_balance_service
        self._show_balance_service = show_balance_service
        self._freeze_balance_service = freeze_balance_service

    @debug_log
    @info_log(strat_info=None, end_info='Баланс открыт')
    def create_balance(self, wallet: 'WalletBase',schema: 'CreateRegularBalanceSchema | CreateForeignBalanceSchema'):
        if schema.key == BalanceTypesEnum.REGULAR:
            return self._create_balance_service.create_regular_balance(schema.key, wallet, schema.amount, schema.currency)
        elif schema.key == BalanceTypesEnum.FOREIGN:
            return self._create_balance_service.create_foreign_balance(schema.key, wallet, schema.amounts, schema.currencies)
        raise

    @debug_log
    @info_log(strat_info='Информация о вашем балансе:', end_info=None)
    def show_regular_balance(self, wallet: 'WalletBase') -> 'BalanceBase':
        return self._show_balance_service.show_balance(wallet)

    @debug_log
    @info_log(strat_info='Информация о ваших балансах:', end_info=None)
    def show_foreign_balance(self, wallet: 'WalletBase') -> 'BalanceBase':
        return self._show_balance_service.show_balances(wallet)

    @debug_log
    @info_log(strat_info=None, end_info='Баланс пользователя заморожен')
    def freeze_regular_balance(self, user: 'UserBase', wallet_id: str):
        return self._freeze_balance_service.freeze_regular_balance(user, wallet_id)

    @debug_log
    @info_log(strat_info=None, end_info='Балансы пользователя заморожены')
    def freeze_foreign_balance(self, user: 'UserBase', wallet_id: str):
        return self._freeze_balance_service.freeze_foreign_balance(user, wallet_id)

    @debug_log
    @info_log(strat_info=None, end_info='Баланс пользователя разморожен')
    def unfreeze_regular_balance(self, user: 'UserBase', wallet_id: str):
        return self._freeze_balance_service.unfreeze_regular_balance(user, wallet_id)

    @debug_log
    @info_log(strat_info=None, end_info='Балансы пользователя разморожены')
    def unfreeze_foreign_balance(self, user: 'UserBase', wallet_id: str):
        return self._freeze_balance_service.unfreeze_foreign_balance(user, wallet_id)


class CreateBalanceService:
    """Класс сервис по созданию баланса"""

    def __init__(self, balance_factory: 'BalanceFactory', balance_commands_repository: 'BalanceCommandsRepository') -> None:
        self._balance_factory = balance_factory
        self._balance_commands_repository = balance_commands_repository

    def create_regular_balance(self, key: 'BalanceTypesEnum', wallet: 'WalletBase', amount: Decimal, currency: str) -> 'BalanceBase':
        obj = self._balance_factory.create_balance(key, wallet.item_id, amount, currency)
        GeneralValidation.not_none_checker(obj)

        try:
            self._balance_commands_repository.insert_balance_info(obj)
        except IntegrityError:
            raise

        return obj

    def create_foreign_balance(self, key: 'BalanceTypesEnum', wallet: 'WalletBase', amounts: list[Decimal], currencies: list[str]) -> 'BalanceBase':
        obj = self._balance_factory.create_balance(key, wallet.item_id, amounts, currencies)
        GeneralValidation.not_none_checker(obj)

        try:
            self._balance_commands_repository.insert_balance_info(obj)
        except IntegrityError:
            raise

        return obj


class ShowBalanceService:
    """Класс сервис по выводу информации о балансе"""

    def __init__(self, wallet_queries_repository: 'WalletQueriesRepository') -> None:
        self._wallet_queries_repository = wallet_queries_repository

    def show_balance(self, wallet: 'WalletBase') -> 'BalanceBase':
        obj = self._wallet_queries_repository.select_my_balance(wallet)
        GeneralValidation.not_none_checker(obj)

        return obj

    def show_balances(self, wallet: 'WalletBase') -> 'BalanceBase':
        obj = self._wallet_queries_repository.select_balances(wallet.item_id)
        GeneralValidation.not_none_checker(obj)

        return obj


class FreezeBalanceService:
    """Класс сервис для заморозки и разморозки баланса"""

    def __init__(self, wallet_queries_repository: 'WalletQueriesRepository', balance_commands_repository: 'BalanceCommandsRepository') -> None:
        self._wallet_queries_repository = wallet_queries_repository
        self._balance_commands_repository = balance_commands_repository

    def freeze_regular_balance(self, user: 'UserBase', wallet_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        obj = self._wallet_queries_repository.select_balance(wallet_id)
        GeneralValidation.not_none_checker(obj)

        if obj.is_frozen:
            raise

        self._balance_commands_repository.upgrade_balance_info(obj, {'is_frozen': True})

    def freeze_foreign_balance(self, user: 'UserBase', wallet_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        obj = self._wallet_queries_repository.select_balances(wallet_id)
        GeneralValidation.not_none_checker(obj)

        if obj.is_frozen:
            raise

        self._balance_commands_repository.upgrade_balance_info(obj, {'is_frozen': True})

    def unfreeze_regular_balance(self, user: 'UserBase', wallet_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        obj = self._wallet_queries_repository.select_balance(wallet_id)
        GeneralValidation.not_none_checker(obj)

        if not obj.is_frozen:
            raise ValueError

        self._balance_commands_repository.upgrade_balance_info(obj, {'is_frozen': False})

    def unfreeze_foreign_balance(self, user: 'UserBase', wallet_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        obj = self._wallet_queries_repository.select_balances(wallet_id)
        GeneralValidation.not_none_checker(obj)

        if not obj.is_frozen:
            raise ValueError

        self._balance_commands_repository.upgrade_balance_info(obj, {'is_frozen': False})


class BalanceOperationsServiceFacade:
    """Класс фасад для управления операциями баланса"""

    def __init__(self, deposit_balance_operation_service: 'DepositBalanceOperationService', withdraw_balance_operation_service: 'WithdrawBalanceOperationService') -> None:
        self._deposit_balance_operation_service = deposit_balance_operation_service
        self._withdraw_balance_operation_service = withdraw_balance_operation_service

    @debug_log
    @info_log(strat_info=None, end_info='Операция прошла успешно')
    def deposit_balance(self, balance: 'BalanceBase', transaction: 'TransactionBase') -> None:
        self._deposit_balance_operation_service.deposit_balance(balance, transaction)

    @debug_log
    @info_log(strat_info=None, end_info='Операция прошла успешно')
    def withdraw_balance(self, balance: 'BalanceBase', transaction: 'TransactionBase') -> None:
        self._withdraw_balance_operation_service.withdraw_balance(balance, transaction)


class DepositBalanceOperationService:
    """Класс сервис для управления операциями по пополнению баланса"""

    def __init__(self, transaction_commands_repository: 'TransactionCommandsRepository', balance_commands_repository: 'BalanceCommandsRepository') -> None:
        self._transaction_commands_repository = transaction_commands_repository
        self._balance_commands_repository = balance_commands_repository

    def deposit_balance(self, balance: 'BalanceBase', transaction: 'TransactionBase') -> None:
        if balance.is_frozen:
            raise ValueError

        self._transaction_commands_repository.update_transaction_info(transaction, {'operation_status': TransactionStatusesEnum.PENDING})
        if transaction.currency != balance.currency:
            raise ValueError("Currency mismatch")

        if balance.balance_type == BalanceTypesEnum.REGULAR:
            try:
                balance.amount += transaction.amount * transaction.fee
            except ValueError:
                self._transaction_commands_repository.update_transaction_info(transaction, {'operation_status': TransactionStatusesEnum.FAILED, 'completed_at': datetime.datetime.now()})
                raise ValueError

            self._transaction_commands_repository.update_transaction_info(transaction, {'operation_status': TransactionStatusesEnum.SUCCESS, 'completed_at': datetime.datetime.now()})
            self._balance_commands_repository.upgrade_balance_info(balance, {'amount': balance.amount})

class WithdrawBalanceOperationService:
    """Класс сервис для управления операциями по снятию денег с баланса"""

    def __init__(self, transaction_commands_repository: 'TransactionCommandsRepository', balance_commands_repository: 'BalanceCommandsRepository') -> None:
        self._transaction_commands_repository = transaction_commands_repository
        self._balance_commands_repository = balance_commands_repository

    def withdraw_balance(self, balance: 'BalanceBase', transaction: 'TransactionBase') -> None:
        if balance.is_frozen:
            raise ValueError

        self._transaction_commands_repository.update_transaction_info(transaction, {'operation_status': TransactionStatusesEnum.PENDING})
        if transaction.currency != balance.currency:
            raise ValueError("Currency mismatch")

        if balance.balance_type == BalanceTypesEnum.REGULAR:
            try:
                balance.amount -= transaction.amount * transaction.fee
            except ValueError:
                self._transaction_commands_repository.update_transaction_info(transaction, {'operation_status': TransactionStatusesEnum.FAILED, 'completed_at': datetime.datetime.now()})
                raise ValueError

            self._transaction_commands_repository.update_transaction_info(transaction, {'operation_status': TransactionStatusesEnum.SUCCESS, 'completed_at': datetime.datetime.now()})
            self._balance_commands_repository.upgrade_balance_info(balance, {'amount': balance.amount})