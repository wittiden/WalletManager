from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.wallets.domain import WalletBase


class WalletRepository:
    """Класс репозиторий для хранения кошельков"""

    def __init__(self) -> None:
        self._wallets: dict[str, 'WalletBase'] = {}

    def add_wallet(self, wallet: 'WalletBase') -> None:
        self._wallets[wallet.item_id] = wallet

    def get_wallet(self, key: str) -> 'WalletBase':
        return self._wallets.get(key)

    def get_all_wallets(self) -> list['WalletBase']:
        return list(self._wallets.values())