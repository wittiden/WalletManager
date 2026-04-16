from typing import TYPE_CHECKING

from app.common.enums.balance_enums import BalanceTypesEnum
from app.database.models import BalanceTable

if TYPE_CHECKING:
    from app.infrastructure.balances.domain import BalanceBase, RegularBalance, ForeignBalance
    from app.infrastructure.balances.factory import BalanceFactory


class BalanceMapper:
    """Mapper класс для преобразования balance->orm_balance, orm_balance->balance"""

    def __init__(self, balance_factory: 'BalanceFactory') -> None:
        self._balance_factory = balance_factory

    def table_to_domain(self, balance_table: 'BalanceTable') -> 'BalanceBase':
        obj = self._balance_factory.create_balance(balance_table.balance_type, balance_table.wallet_id, balance_table.amount, balance_table.currency)
        obj.is_frozen = balance_table.is_frozen
        obj.item_id = balance_table.balance_id
        return obj

    def tables_to_domain(self, balance_tables: list['BalanceTable']) -> 'BalanceBase':
        currencies = []
        amounts = []
        for balance_table in balance_tables:
            currencies.append(balance_table.currency)
            amounts.append(balance_table.amount)

        for balance_table in balance_tables:
            obj = self._balance_factory.create_balance(balance_table.balance_type, balance_table.wallet_id, amounts, currencies)
            obj.is_frozen = balance_table.is_frozen
            obj.item_id = balance_table.balance_id
            return obj
        raise

    @staticmethod
    def domain_to_table(balance: 'RegularBalance') -> 'BalanceTable':
        if balance.balance_type == BalanceTypesEnum.REGULAR:
            return BalanceTable(balance_id=balance.item_id, wallet_id=balance.wallet_id, is_frozen=balance.is_frozen, balance_type=balance.balance_type, currency=balance.currency, amount=balance.amount)
        raise

    @staticmethod
    def domain_to_tables(balance: 'ForeignBalance') -> list['BalanceTable']:
        if balance.balance_type == BalanceTypesEnum.FOREIGN:

            return [BalanceTable(balance_id=balance.item_id, wallet_id=balance.wallet_id, is_frozen=balance.is_frozen, balance_type=balance.balance_type, currency=currency, amount=amount) for currency, amount in zip(balance.currencies, balance.amounts)]
        raise