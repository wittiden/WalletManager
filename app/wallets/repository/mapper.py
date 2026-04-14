from app.common.enums.wallet_enums import WalletTypesEnum
from app.database.models.wallet import WalletTable, BalanceTable
from app.wallets.domain import WalletBase, RegularWallet, ForeignWallet


class WalletMapper:
    """"""

    @staticmethod
    def domain_to_table(wallet: 'WalletBase') -> 'WalletTable':
        pass

    @staticmethod
    def table_to_domain(wallet_table: 'RegularWallet', balance_table: 'BalanceTable') -> 'WalletBase':
        if wallet_table.status == WalletTypesEnum.REGULAR:
            obj = RegularWallet(_pin=wallet_table.pin, _owner=wallet_table.owner, _regular_balance_currency=balance_table.balance_currency)
            obj.is_blocked = wallet_table.is_blocked
            obj.balance[balance_table.balance_currency.name] = balance_table.balance_amount

        # elif wallet_table.status == WalletTypesEnum.FOREIGN:
        #     currencies_list = []
        #
        #     balance =
        #
        #
        #     obj = ForeignWallet(_pin=wallet_table.pin, _owner=wallet_table.owner)
