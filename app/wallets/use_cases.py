from typing import Any, TYPE_CHECKING

from app.core.enums.wallet_enums import WalletTypesEnum
from app.core.validations.exceptions import WalletIsBlockedError, WalletIsNotBlockedError, WalletIsNotClose, \
    AllParametersIsNoneError
from app.core.validations.general_validations import UseCasesValidation, GeneralValidation
from app.wallets.domain import WalletBase
from app.core.utils.decorators import debug_log, info_log

if TYPE_CHECKING:
    from app.users.domain import UserBase
    from app.wallets.factory import WalletFactory
    from app.wallets.repository import WalletRepository
    from app.wallets.strategy import WalletStrategy


class WalletServiceFacade:
    """Класс фасад для управления сервисами кошельков"""

    def __init__(self, create_wallet_service: 'CreateWalletService', show_wallet_service: 'ShowWalletService', sort_wallet_service: 'SortWalletService', block_wallet_service: 'BlockWalletService', close_wallet_service: 'CloseWalletService') -> None:
        self._create_wallet_service = create_wallet_service
        self._show_wallet_service = show_wallet_service
        self._sort_wallet_service = sort_wallet_service
        self._block_wallet_service = block_wallet_service
        self._close_wallet_service = close_wallet_service

    @debug_log
    @info_log(['','Пользователь создан'])
    def create_wallet(self, user: 'UserBase', key: 'WalletTypesEnum', pin: str, balance_currency: Any, strategy: 'WalletStrategy' = None) -> 'WalletBase':
        return self._create_wallet_service.create_wallet(user, key, pin, balance_currency, strategy)

    @debug_log
    @info_log(['Информация о кошельке:',''])
    def show_wallet(self, user: 'UserBase', find_wallet_id: str) -> WalletBase:
        return self._show_wallet_service.show_wallet(user, find_wallet_id)

    @debug_log
    @info_log(['Информация о вашем кошельке:',''])
    def show_my_wallets(self, user: 'UserBase') -> list['WalletBase']:
        return self._show_wallet_service.show_my_wallets(user)

    @debug_log
    @info_log(['Информация о кошельках:',''])
    def show_all_wallets(self, user: 'UserBase') -> list['WalletBase']:
        return self._show_wallet_service.show_all_wallets(user)

    @debug_log
    @info_log(['Отсортированные кошельки:',''])
    def sort_wallets(self, user: 'UserBase', pin: bool = None, is_blocked: bool = None, owner: bool = None, status: bool = None, address: bool = None) -> list['WalletBase']:
        return self._sort_wallet_service.sort_wallets(user, pin, is_blocked, owner, status, address)

    @debug_log
    @info_log(['','Кошелек заблокирован'])
    def block_wallet(self, user: 'UserBase', find_user_id: str) -> None:
        self._block_wallet_service.block_wallet(user, find_user_id)

    @debug_log
    @info_log(['','Кошелек разблокирован'])
    def unblock_wallet(self, user: 'UserBase', find_user_id: str) -> None:
        self._block_wallet_service.unblock_wallet(user, find_user_id)

    @debug_log
    @info_log(['','Кошелек закрыт и удален с вашего аккаунта'])
    def close_wallet(self, user: 'UserBase', wallet_id: str, pin: str) -> None:
        self._close_wallet_service.close_my_wallet(user, wallet_id, pin)


class CreateWalletService:
    """Класс сервис по созданию кошельков"""

    def __init__(self, wallet_repository: 'WalletRepository', wallet_factory: 'WalletFactory') -> None:
        self._wallet_repository = wallet_repository
        self._wallet_factory = wallet_factory

    def create_wallet(self, user: 'UserBase', key: 'WalletTypesEnum', pin: str, balance_currency: Any, strategy: 'WalletStrategy' = None) -> 'WalletBase':
        UseCasesValidation.is_client_checker(user)

        if key == WalletTypesEnum.REGULAR:
            GeneralValidation.not_none_checker(strategy)
            wallet = self._wallet_factory.create_wallet(key, pin, balance_currency, strategy)

        elif key == WalletTypesEnum.FOREIGN:
            wallet = self._wallet_factory.create_wallet(key, pin, balance_currency)

        GeneralValidation.not_none_checker(wallet)

        user._wallets.append(wallet)
        wallet.owner = user
        self._wallet_repository.add_wallet(wallet)

        return wallet


class ShowWalletService:
    """Класс сервис для вывода информации о кошельках"""

    def __init__(self, wallet_repository: 'WalletRepository') -> None:
        self._wallet_repository = wallet_repository

    def show_all_wallets(self, user: 'UserBase') -> list['WalletBase']:
        UseCasesValidation.is_admin_checker(user)

        return GeneralValidation.not_none_checker(self._wallet_repository.get_all_wallets())

    @staticmethod
    def show_my_wallets(user: 'UserBase') -> list['WalletBase']:
        UseCasesValidation.is_client_checker(user)

        return [GeneralValidation.not_none_checker(wallet) for wallet in user.wallets]

    def show_wallet(self, user: 'UserBase', find_wallet_id: str) -> 'WalletBase':
        UseCasesValidation.is_admin_checker(user)

        return GeneralValidation.not_none_checker(self._wallet_repository.get_wallet(find_wallet_id))


class BlockWalletService:
    """Класс сервис по блокировке или разблокировке кошельков"""

    def __init__(self, wallet_repository: 'WalletRepository') -> None:
        self._wallet_repository = wallet_repository

    def block_wallet(self, user: 'UserBase', find_wallet_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        find_wallet = GeneralValidation.not_none_checker(self._wallet_repository.get_wallet(find_wallet_id))

        if find_wallet.is_blocked:
            raise WalletIsBlockedError

        find_wallet.is_blocked = True

    def unblock_wallet(self, user: 'UserBase', find_wallet_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        find_wallet = GeneralValidation.not_none_checker(self._wallet_repository.get_wallet(find_wallet_id))

        if not find_wallet.is_blocked:
            raise WalletIsNotBlockedError

        find_wallet.is_blocked = False


class CloseWalletService:
    """Класс сервис по закрытию кошельков"""

    def __init__(self, wallet_repository: 'WalletRepository') -> None:
        self._wallet_repository = wallet_repository

    def close_my_wallet(self, user: 'UserBase', wallet_id: str, pin: str):
        UseCasesValidation.is_client_checker(user)

        my_wallet = self._wallet_repository.get_wallet(wallet_id)

        if not my_wallet.owner.item_id == user.item_id:
            raise WalletIsNotClose

        if pin == my_wallet.pin:
            raise WalletIsNotClose

        self._wallet_repository.del_wallet(my_wallet.item_id)
        user.wallets.remove(my_wallet)


class SortWalletService:
    """Класс сервис по сортировке кошельков"""

    def __init__(self, wallet_repository: 'WalletRepository') -> None:
        self._wallet_repository = wallet_repository

    def sort_wallets(self, user: 'UserBase', pin: bool = None, is_blocked: bool = None, owner: bool = None, status: bool = None, address: bool = None):
        UseCasesValidation.is_admin_checker(user)

        all_wallets = self._wallet_repository.get_all_wallets()

        param_dict = {'pin': pin, 'is_blocked': is_blocked, 'owner': owner, 'status': status, 'address': address}
        for key, value in param_dict.items():
            if value:
                return sorted(all_wallets, key=lambda r : getattr(r, key))

        raise AllParametersIsNoneError


class WalletOperationsFacade:
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
