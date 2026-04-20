from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING

from app.common.enums.balance_enums import BalanceTypesEnum
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
    def show_balance(self, wallet: 'WalletBase') -> 'BalanceBase':
        return self._show_balance_service.show_balance(wallet)

    @debug_log
    @info_log(strat_info=None, end_info='Баланс пользователя заморожен')
    def freeze_balance(self, user: 'UserBase', wallet_id: str):
        return self._freeze_balance_service.freeze_balance(user, wallet_id)

    @debug_log
    @info_log(strat_info=None, end_info='Баланс пользователя разморожен')
    def unfreeze_balance(self, user: 'UserBase', wallet_id: str):
        return self._freeze_balance_service.unfreeze_balance(user, wallet_id)


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


class FreezeBalanceService:
    """Класс сервис для заморозки и разморозки баланса"""

    def __init__(self, wallet_queries_repository: 'WalletQueriesRepository', balance_commands_repository: 'BalanceCommandsRepository') -> None:
        self._wallet_queries_repository = wallet_queries_repository
        self._balance_commands_repository = balance_commands_repository

    def freeze_balance(self, user: 'UserBase', wallet_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        obj = self._wallet_queries_repository.select_balances(wallet_id)
        GeneralValidation.not_none_checker(obj)

        if obj.is_frozen:
            raise

        self._balance_commands_repository.upgrade_balance_info(obj, {'is_frozen': True})

    def unfreeze_balance(self, user: 'UserBase', wallet_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        obj = self._wallet_queries_repository.select_balances(wallet_id)
        GeneralValidation.not_none_checker(obj)

        if not obj.is_frozen:
            raise

        self._balance_commands_repository.upgrade_balance_info(obj, {'is_frozen': False})


# class WalletOperationsServiceFacade:
#     """Класс фасад для управления операциями кошельков"""
#
#     def __init__(self, deposit_wallet_operation_service: 'DepositWalletOperationService', withdraw_wallet_operation_service: 'WithdrawWalletOperationService', exchange_wallet_operation_service: 'ExchangeWalletOperationService') -> None:
#         self._deposit_wallet_operation_service = deposit_wallet_operation_service
#         self._withdraw_wallet_operation_service = withdraw_wallet_operation_service
#         self._exchange_wallet_operation_service = exchange_wallet_operation_service
#
#     def deposit_wallet(self):
#         pass
#
#     def withdraw_wallet(self):
#         pass
#
#     def exchange_currencies_wallet(self):
#         pass
#
#
# class DepositWalletOperationService:
#     """Класс сервис для управления операциями по пополнению кошелька"""
#
#     @staticmethod
#     def deposit_wallet(balance: 'RegularBalance', transaction: 'DepositTransaction'):
#         if balance.is_frozen:
#             raise ValueError
#
#         # if RegularBalance:
#         #     transaction.operation_status.PENDING
#         #     try:
#         #         balance[transaction.deposit_currency] += transaction.amount
#         #     except ValueError:
#         #         transaction.operation_status.FAILED
#         #         raise
#         #     transaction.operation_status.SUCCESS
#         # if ForeignBalance:
#
#
# class WithdrawWalletOperationService:
#     """Класс сервис для управления операциями по снятию денег с кошелька"""
#
#     @staticmethod
#     def withdraw_wallet(balance: 'RegularBalance'):
#         pass
#
# class ExchangeWalletOperationService:
#     """Класс сервис для управления операциями по обмену валют на кошельке"""
#
#     @staticmethod
#     def exchange_wallet():
#         pass