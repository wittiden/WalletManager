from typing import Any, TYPE_CHECKING

from app.core.enums.wallet_enums import WalletTypesEnum, WalletBalanceCurrenciesEnum
from app.core.utils.general_funcs import get_hash
from app.core.validations.exceptions import WalletIsBlockedError, WalletIsNotBlockedError, WalletIsNotClose, \
    AllParametersIsNoneError, UnknownWalletTypeError
from app.core.validations.general_validations import UseCasesValidation, GeneralValidation
from app.wallets.domain import WalletBase
from app.core.utils.decorators import debug_log, info_log
from app.wallets.schemas import CreateRegularWalletSchema, CreateForeignWalletSchema, CloseWalletSchema

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
    def create_wallet(self, user: 'UserBase', schema: 'CreateRegularWalletSchema | CreateForeignWalletSchema') -> 'WalletBase':
        if isinstance(schema, CreateRegularWalletSchema):
            return self._create_wallet_service.create_regular_wallet(user, schema.key, schema.pin, schema.balance_currency, schema.strategy)
        elif isinstance(schema, CreateForeignWalletSchema):
            return self._create_wallet_service.create_foreign_wallet(user, schema.key, schema.pin, schema.balance_currency)

        raise UnknownWalletTypeError

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
    def sort_wallets(self, user: 'UserBase', is_blocked: bool = None, owner: bool = None, status: bool = None, address: bool = None) -> list['WalletBase']:
        return self._sort_wallet_service.sort_wallets(user, is_blocked, owner, status, address)

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
    def close_wallet(self, user: 'UserBase', schema: 'CloseWalletSchema') -> None:
        self._close_wallet_service.close_my_wallet(user, schema.wallet_id, schema.pin)


class CreateWalletService:
    """Класс сервис по созданию кошельков"""

    def __init__(self, wallet_repository: 'WalletRepository', wallet_factory: 'WalletFactory') -> None:
        self._wallet_repository = wallet_repository
        self._wallet_factory = wallet_factory

    def create_regular_wallet(self, user: 'UserBase', key: 'WalletTypesEnum', pin: str, balance_currency: 'WalletBalanceCurrenciesEnum', strategy: 'WalletStrategy') -> 'WalletBase':
        UseCasesValidation.is_client_checker(user)

        wallet = self._wallet_factory.create_wallet(key, get_hash(pin), balance_currency, strategy)

        GeneralValidation.not_none_checker(wallet)

        user._wallets.append(wallet)
        wallet.owner = user
        self._wallet_repository.add_wallet(wallet)

        return wallet

    def create_foreign_wallet(self, user: 'UserBase', key: 'WalletTypesEnum', pin: str, balance_currency: list['WalletBalanceCurrenciesEnum']) -> 'WalletBase':
        UseCasesValidation.is_client_checker(user)

        wallet = self._wallet_factory.create_wallet(key, get_hash(pin), balance_currency)

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

        if get_hash(pin) != my_wallet.pin:
            raise WalletIsNotClose

        self._wallet_repository.del_wallet(my_wallet.item_id)
        user.wallets.remove(my_wallet)


class SortWalletService:
    """Класс сервис по сортировке кошельков"""

    def __init__(self, wallet_repository: 'WalletRepository') -> None:
        self._wallet_repository = wallet_repository

    def sort_wallets(self, user: 'UserBase', is_blocked: bool = None, owner: bool = None, status: bool = None, address: bool = None):
        UseCasesValidation.is_admin_checker(user)

        all_wallets = self._wallet_repository.get_all_wallets()

        param_dict = {'is_blocked': is_blocked, 'owner': owner, 'status': status, 'address': address}
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
