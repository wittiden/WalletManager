from dataclasses import dataclass, field
from decimal import Decimal

from blinker import Signal

from app.common.enums.balance_enums import BalanceTypesEnum
from app.common.mixins import MixinId
from app.core.invariants import DomainInvariant
from app.core.utils import blink_func

upgrade_balance_signal = Signal()
upgrade_balance_signal.connect(blink_func)


@dataclass
class BalanceBase(MixinId):
    """Базовый класс для хранения данных баланса"""

    _wallet_id: str
    _balance: dict[str, Decimal] = field(default=None, init=False)
    _is_frozen: bool = field(default=False, init=False)
    _balance_type: 'BalanceTypesEnum' = field(default=BalanceTypesEnum.UNKNOWN, init=False)

    def __post_init__(self) -> None:
        super().__init__()

        DomainInvariant.no_empty('wallet_id', self._wallet_id)
        DomainInvariant.is_instance('is_frozen', self._is_frozen, bool)

    @property
    def wallet_id(self) -> str:
        return self._wallet_id

    @property
    def is_frozen(self) -> bool:
        return self._is_frozen

    @property
    def balance_type(self) -> 'BalanceTypesEnum':
        return self._balance_type

    @property
    def balance(self) -> dict[str, Decimal]:
        return self._balance

    @is_frozen.setter
    def is_frozen(self, value: bool) -> None:
        self._is_frozen = DomainInvariant.is_instance('is_frozen', value, bool)

    @balance.setter
    def balance(self, value: dict[str, Decimal]) -> None:
        self._balance = value

    @wallet_id.setter
    def wallet_id(self, value: str) -> None:
        old_value = self._wallet_id
        self._wallet_id = DomainInvariant.no_empty('wallet_id', value)
        upgrade_balance_signal.send(self, field='wallet_id', old=old_value, new=value)

    def __repr__(self) -> str:
        return f'{self._balance_type.value} #{self.item_id} -> wallet_id: #{self._wallet_id}, is_frozen: {self._is_frozen}'

    __str__ = __repr__


@dataclass
class RegularBalance(BalanceBase):
    """Класс для хранения данных обычного баланса"""

    _amount: Decimal
    _currency: str

    def __post_init__(self) -> None:
        super().__post_init__()

        self._balance_type = BalanceTypesEnum.REGULAR
        DomainInvariant.no_negative('amount', self._amount)
        DomainInvariant.no_empty('currency', self._currency)

        self._balance: dict[str, Decimal] = {self._currency: self._amount}

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> str:
        return self._currency

    @amount.setter
    def amount(self, value: Decimal) -> None:
        self._amount = DomainInvariant.no_negative('amount', value)

    @currency.setter
    def currency(self, value: str) -> None:
        self._currency = DomainInvariant.no_empty('currency', value)

    def __repr__(self) -> str:
        return f'{super().__repr__()}\n{self._balance}'

    __str__ = __repr__


@dataclass
class ForeignBalance(BalanceBase):
    """Класс для хранения данных валютного баланса"""

    _amounts: list[Decimal]
    _currencies: list[str]

    def __post_init__(self) -> None:
        super().__post_init__()

        self._balance_type = BalanceTypesEnum.FOREIGN

        DomainInvariant.no_empty_collection('amounts', self._amounts)
        DomainInvariant.no_empty_collection('currencies', self._currencies)

        self._balance: dict[str, Decimal] = {currency: amount for amount, currency in zip(self._amounts, self._currencies)}

    @property
    def amounts(self) -> list[Decimal]:
        return self._amounts

    @property
    def currencies(self) -> list[str]:
        return self._currencies

    @amounts.setter
    def amounts(self, value: list[Decimal]) -> None:
        self._amounts = DomainInvariant.no_empty_collection('amounts', value)

    @currencies.setter
    def currencies(self, value: list[str]) -> None:
        self._currencies = DomainInvariant.no_empty_collection('currencies', value)

    def __repr__(self) -> str:
        return f'{super().__repr__()}\n{self._balance}'

    __str__ = __repr__
