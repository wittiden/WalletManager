from typing import TYPE_CHECKING

from app.common.enums.wallet_enums import WalletTypesEnum
from app.database.models.wallet import WalletTable, BalanceTable

if TYPE_CHECKING:
    from app.users.domain import UserBase
    from app.wallets.domain import WalletBase
    from app.wallets.factory import WalletFactory


class WalletMapper:
    """Mapper класс для преобразования wallet->orm_wallet, orm_wallet->wallet"""

    def __init__(self, wallet_factory: 'WalletFactory') -> None:
        self._wallet_factory = wallet_factory

    @staticmethod
    def domain_to_table(wallet: 'WalletBase') -> 'WalletTable':
        return WalletTable(wallet_id=wallet.item_id, pin=wallet.pin, address=wallet.address, owner_id=wallet.owner.item_id, status=wallet.status, is_blocked=wallet.is_blocked)

    def table_to_domain(self, wallet_table: 'WalletTable', balances: list['BalanceTable'], user: 'UserBase') -> 'WalletBase':
        if wallet_table.status == WalletTypesEnum.REGULAR:
            obj = self._wallet_factory.create_wallet(wallet_table.status, wallet_table.pin, user, balances[0].balance_currency)
            obj.balance[obj.balance_currency.name] = balances[0].balance_amount

        elif wallet_table.status == WalletTypesEnum.FOREIGN:
            obj = self._wallet_factory.create_wallet(wallet_table.status, wallet_table.pin, user,[balance.balance_currency for balance in balances])
            for balance in balances:
                obj.balance[balance.balance_currency.name] = balance.balance_amount
        else:
            raise ValueError(f"Unknown status: {wallet_table.status}")

        obj.is_blocked = wallet_table.is_blocked

        return obj


class BalanceMapper:
    """Mapper класс для преобразования balance->orm_balance, orm_balance->balance"""

    @staticmethod
    def domain_to_table(wallet: 'WalletBase') -> list['BalanceTable']:
        return [BalanceTable( wallet_id=wallet.item_id, balance_currency=currency, balance_amount=amount) for currency, amount in wallet.balance.items()]