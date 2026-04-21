from typing import TYPE_CHECKING

from app.database.models.wallet import WalletTable

if TYPE_CHECKING:
    from app.infrastructure.wallets.domain import WalletBase
    from app.infrastructure.wallets.factory import WalletFactory


class WalletMapper:
    """Mapper класс для преобразования wallet->orm_wallet, orm_wallet->wallet"""

    def __init__(self, wallet_factory: 'WalletFactory') -> None:
        self._wallet_factory = wallet_factory

    @staticmethod
    def domain_to_table(wallet: 'WalletBase') -> 'WalletTable':
        return WalletTable(
            wallet_id=wallet.item_id, pin=wallet.pin, owner_id=wallet.owner_id, address=wallet.address, is_blocked=wallet.is_blocked, account_type=wallet.account_type
        )

    def table_to_domain(self, wallet_table: 'WalletTable') -> 'WalletBase':
        if wallet_table is None:
            raise ValueError

        obj = self._wallet_factory.create_wallet(wallet_table.account_type, wallet_table.pin, wallet_table.owner_id)
        obj.is_blocked = wallet_table.is_blocked
        obj.address = wallet_table.address
        obj.item_id = wallet_table.wallet_id

        return obj
