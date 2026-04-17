from typing import TYPE_CHECKING
from sqlalchemy.exc import IntegrityError

from app.common.enums.wallet_enums import WalletTypesEnum
from app.core.decorators import debug_log, info_log
from app.core.exceptions import WalletIsBlockedError, WalletIsNotBlockedError
from app.core.utils import get_hash
from app.core.validations import UseCasesValidation, GeneralValidation

if TYPE_CHECKING:
    from app.infrastructure.users.domain import UserBase
    from app.infrastructure.wallets.factory import WalletFactory
    from app.infrastructure.wallets.schemas import CreateWalletSchema, CloseWalletSchema
    from app.infrastructure.wallets.repository.commands import WalletCommandsRepository
    from app.infrastructure.wallets.repository.queries import WalletQueriesRepository
    from app.infrastructure.wallets.domain import WalletBase
    from app.infrastructure.users.repository.commands import UserCommandsRepository


class WalletServiceFacade:
    """Класс фасад для управления сервисами кошельков"""

    def __init__(self, create_wallet_service: 'CreateWalletService', show_wallet_service: 'ShowWalletService', sort_wallet_service: 'SortWalletService', block_wallet_service: 'BlockWalletService', close_wallet_service: 'CloseWalletService') -> None:
        self._create_wallet_service = create_wallet_service
        self._show_wallet_service = show_wallet_service
        self._sort_wallet_service = sort_wallet_service
        self._block_wallet_service = block_wallet_service
        self._close_wallet_service = close_wallet_service

    @debug_log
    @info_log(strat_info=None, end_info='Счет создан')
    def create_wallet(self, user: 'UserBase', schema: 'CreateWalletSchema') -> 'WalletBase':
        return self._create_wallet_service.create_wallet(user, schema.key, schema.pin)

    @debug_log
    @info_log(strat_info='Информация о счете пользователя:', end_info=None)
    def show_wallet(self, user: 'UserBase', find_wallet_id: str) -> 'WalletBase':
        return self._show_wallet_service.show_wallet(user, find_wallet_id)

    @debug_log
    @info_log(strat_info='Информация о ваших счетах:', end_info=None)
    def show_my_wallets(self, user: 'UserBase') -> list['WalletBase']:
        return self._show_wallet_service.show_my_wallets(user)

    @debug_log
    @info_log(strat_info='Информация о счетах пользователей:', end_info=None)
    def show_all_wallets(self, user: 'UserBase') -> list['WalletBase']:
        return self._show_wallet_service.show_all_wallets(user)

    @debug_log
    @info_log(strat_info='Отсортированная информация о счетах пользователей:', end_info=None)
    def sort_all_wallets(self, user: 'UserBase', order_by_param: str) -> list['WalletBase']:
        return self._sort_wallet_service.sort_all_wallets(user, order_by_param)

    @debug_log
    @info_log(strat_info='Отсортированная информация о счете пользователя:', end_info=None)
    def sort_my_wallets(self, user: 'UserBase', order_by_param: str) -> list['WalletBase']:
        return self._sort_wallet_service.sort_my_wallets(user, order_by_param)

    @debug_log
    @info_log(strat_info=None, end_info='Счет пользователя заблокирован')
    def block_wallet(self, user: 'UserBase', find_user_id: str) -> None:
        self._block_wallet_service.block_wallet(user, find_user_id)

    @debug_log
    @info_log(strat_info=None, end_info='Счет пользователя разблокирован')
    def unblock_wallet(self, user: 'UserBase', find_user_id: str) -> None:
        self._block_wallet_service.unblock_wallet(user, find_user_id)

    @debug_log
    @info_log(strat_info=None, end_info='Ваш счет закрыт')
    def close_wallet(self, user: 'UserBase', schema: 'CloseWalletSchema') -> None:
        self._close_wallet_service.close_my_wallet(user, schema.pin, schema.address)


class CreateWalletService:
    """Класс сервис по созданию кошельков"""

    def __init__(self, wallet_factory: 'WalletFactory', wallet_commands_repository: 'WalletCommandsRepository', user_commands_repository: 'UserCommandsRepository') -> None:
        self._wallet_factory = wallet_factory
        self._wallet_commands_repository = wallet_commands_repository

    def create_wallet(self, user: 'UserBase', key: 'WalletTypesEnum', pin: str) -> 'WalletBase':
        UseCasesValidation.is_client_checker(user)

        obj = self._wallet_factory.create_wallet(key, get_hash(pin), user.item_id)
        GeneralValidation.not_none_checker(obj)

        try:
            self._wallet_commands_repository.insert_wallet_info(obj)

        except IntegrityError:
            raise

        return obj


class ShowWalletService:
    """Класс сервис для вывода информации о кошельках"""

    def __init__(self, wallet_queries_repository: 'WalletQueriesRepository') -> None:
        self._wallet_queries_repository = wallet_queries_repository

    def show_all_wallets(self, user: 'UserBase') -> list['WalletBase']:
        UseCasesValidation.is_admin_checker(user)

        return self._wallet_queries_repository.select_all_wallets()

    def show_my_wallets(self, user: 'UserBase') -> list['WalletBase']:
        UseCasesValidation.is_client_checker(user)

        return self._wallet_queries_repository.select_my_wallets(user)

    def show_wallet(self, user: 'UserBase', find_wallet_id: str) -> 'WalletBase':
        UseCasesValidation.is_admin_checker(user)

        return GeneralValidation.not_none_checker(self._wallet_queries_repository.select_wallet(find_wallet_id))


class SortWalletService:
    """Класс сервис по сортировке кошельков"""

    def __init__(self, wallet_queries_repository: 'WalletQueriesRepository') -> None:
        self._wallet_queries_repository = wallet_queries_repository

    def sort_all_wallets(self, user: 'UserBase', order_by_param: str) -> list['WalletBase']:
        UseCasesValidation.is_admin_checker(user)

        return self._wallet_queries_repository.select_order_by_all_wallets(order_by_param)

    def sort_my_wallets(self, user: 'UserBase', order_by_param: str) -> list['WalletBase']:
        UseCasesValidation.is_client_checker(user)

        return self._wallet_queries_repository.select_order_by_my_wallets(user, order_by_param)


class BlockWalletService:
    """Класс сервис по блокировке или разблокировке кошельков"""

    def __init__(self, wallet_commands_repository: 'WalletCommandsRepository', wallet_queries_repository: 'WalletQueriesRepository') -> None:
        self._wallet_commands_repository = wallet_commands_repository
        self._wallet_queries_repository = wallet_queries_repository

    def block_wallet(self, user: 'UserBase', find_wallet_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        obj = GeneralValidation.not_none_checker(self._wallet_queries_repository.select_wallet(find_wallet_id))

        if obj.is_blocked:
            raise WalletIsBlockedError

        self._wallet_commands_repository.update_wallet_info(obj,{'is_blocked': True})

    def unblock_wallet(self, user: 'UserBase', find_wallet_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        obj = GeneralValidation.not_none_checker(self._wallet_queries_repository.select_wallet(find_wallet_id))

        if not obj.is_blocked:
            raise WalletIsNotBlockedError

        self._wallet_commands_repository.update_wallet_info(obj,{'is_blocked': False})


class CloseWalletService:
    """Класс сервис по закрытию кошельков"""

    def __init__(self, wallet_commands_repository: 'WalletCommandsRepository', wallet_queries_repository: 'WalletQueriesRepository') -> None:
        self._wallet_commands_repository = wallet_commands_repository
        self._wallet_queries_repository = wallet_queries_repository

    def close_my_wallet(self, user: 'UserBase', pin: str, address: str) -> None:
        UseCasesValidation.is_client_checker(user)

        obj = GeneralValidation.not_none_checker(self._wallet_queries_repository.select_for_close_wallet(user, get_hash(pin), address))
        self._wallet_commands_repository.delete_wallet_info(GeneralValidation.not_none_checker(obj))


class WalletOperationsServiceFacade:
    """Класс фасад для управления операциями кошельков"""

    def __init__(self, deposit_wallet_operation_service: 'DepositWalletOperationService', withdraw_wallet_operation_service: 'WithdrawWalletOperationService', exchange_wallet_operation_service: 'ExchangeWalletOperationService') -> None:
        self._deposit_wallet_operation_service = deposit_wallet_operation_service
        self._withdraw_wallet_operation_service = withdraw_wallet_operation_service
        self._exchange_wallet_operation_service = exchange_wallet_operation_service

    def deposit_wallet(self):
        pass

    def withdraw_wallet(self):
        pass

    def exchange_currencies_wallet(self):
        pass


class DepositWalletOperationService:
    """Класс сервис для управления операциями по пополнению кошелька"""


class WithdrawWalletOperationService:
    """Класс сервис для управления операциями по снятию денег с кошелька"""


class ExchangeWalletOperationService:
    """Класс сервис для управления операциями по обмену валют на кошельке"""
