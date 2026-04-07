from typing import Any, TYPE_CHECKING

from app.core.enums.wallet_enums import WalletTypesEnum
from app.core.validations.general_validations import UseCasesValidation, GeneralValidation

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

    def create_wallet(self):
        pass

    def show_wallet(self):
        pass

    def show_my_wallet(self):
        pass

    def show_all_wallets(self):
        pass

    def show_and_sort_wallets(self):
        pass

    def block_wallet(self):
        pass

    def unblock_wallet(self):
        pass

    def close_wallet(self):
        pass


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

class CreateWalletService:
    """"""

    def __init__(self, wallet_repository: 'WalletRepository', wallet_factory: 'WalletFactory') -> None:
        self._wallet_repository = wallet_repository
        self._wallet_factory = wallet_factory

    def create_wallet(self, user: 'UserBase', key: 'WalletTypesEnum', password: str, balance_currency: Any, strategy: 'WalletStrategy' = None):
        UseCasesValidation.is_client_checker(user)

        if key == WalletTypesEnum.REGULAR:
            if strategy is None:
                raise ValueError
            wallet = self._wallet_factory.create_wallet(key, password, balance_currency, strategy)

        elif key == WalletTypesEnum.FOREIGN:
            wallet = self._wallet_factory.create_wallet(key, password, balance_currency)

        GeneralValidation.not_none_checker(wallet)

        user._wallets.append(wallet)
        wallet.owner = user
        self._wallet_repository.add_wallet(wallet)

        return wallet


class DepositWalletOperationService:
    """"""


class WithdrawWalletOperationService:
    """"""


class ShowWalletService:
    """"""


class SortWalletService:
    """"""


class ExchangeWalletOperationService:
    """"""


class BlockWalletService:
    """"""


class CloseWalletService:
    """"""