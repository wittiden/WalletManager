from typing import TYPE_CHECKING

from app.core.validations.exceptions import ElementNotFoundError

if TYPE_CHECKING:
    from app.wallets.domain import WalletBase


class WalletRepository:
    """Класс репозиторий для хранения кошельков"""

    def __init__(self) -> None:
        self._wallets: dict[str, 'WalletBase'] = {}

    def add_wallet(self, wallet: 'WalletBase') -> None:
        self._wallets[wallet.item_id] = wallet

    def get_wallet(self, wallet_id: str) -> 'WalletBase':
        return self._wallets.get(wallet_id)

    def get_all_wallets(self) -> list['WalletBase']:
        return list(self._wallets.values())

    def del_wallet(self, wallet_id: str) -> None:
        if not wallet_id in self._wallets.keys():
            raise ElementNotFoundError(f'wallet #{wallet_id} not found')

        del self._wallets[wallet_id]
