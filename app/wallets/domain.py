import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from typing import TYPE_CHECKING, ParamSpec
from blinker import Signal

from app.common.enums.wallet_enums import WalletBalanceCurrenciesEnum
from app.common.enums.wallet_enums import WalletTypesEnum
from app.common.mixins import MixinId
from app.core.invariants import DomainInvariant
from app.core.utils import blink_func

if TYPE_CHECKING:
    from app.users.domain import UserBase

P = ParamSpec('P')

wallet_upgrade_signal = Signal()
wallet_upgrade_signal.connect(blink_func)


@dataclass
class WalletBase(MixinId):
    """Базовый класс для хранения данных кошелька"""

    _pin: str
    _owner: 'UserBase'
    _is_blocked: bool = field(default=False, init=False)
    _status: 'WalletTypesEnum' = field(default=WalletTypesEnum.UNKNOWN, init=False)

    def __post_init__(self) -> None:
        super().__init__()

        DomainInvariant.no_empty('pin', self._pin)

        self._address: str = uuid.uuid4().hex[:26]

    @property
    def pin(self) -> str:
        return self._pin

    @property
    def status(self) -> 'WalletTypesEnum':
        return self._status

    @property
    def is_blocked(self) -> bool:
        return self._is_blocked

    @property
    def owner(self) -> 'UserBase':
        return self._owner

    @property
    def address(self) -> str:
        return self._address

    @pin.setter
    def pin(self, value: str) -> None:
        self._pin = DomainInvariant.no_empty('pin', value)

    @owner.setter
    def owner(self, value: 'UserBase') -> None:
        old_value = self._owner
        self._owner = DomainInvariant.no_none('owner', value)
        wallet_upgrade_signal.send(self, field='owner', old=old_value, new=value)

    @is_blocked.setter
    def is_blocked(self, value: 'bool') -> None:
        old_value = self._is_blocked
        self._is_blocked = DomainInvariant.is_instance('is_blocked', value, bool)
        wallet_upgrade_signal.send(self, field='is_blocked', old=old_value, new=value)

    def __repr__(self) -> str:
        return f'{self.status.value} #{self.item_id} - owner: {self._owner.status if self._owner else 'кошелек не имеет привязки'} #{self._owner.item_id if self._owner else 'None'}\nAddress: {self._address}, is_blocked: {self._is_blocked}'

    __str__ = __repr__


@dataclass
class RegularWallet(WalletBase):
    """Класс для хранения данных обычного кошелька"""

    _regular_balance_currency: 'WalletBalanceCurrenciesEnum'

    def __post_init__(self) -> None:
        super().__post_init__()

        DomainInvariant.is_instance('regular_balance_currency', self._regular_balance_currency, WalletBalanceCurrenciesEnum)

        self._balance: dict[str, Decimal] = {self._regular_balance_currency.name: Decimal('0.00')}
        self._status = WalletTypesEnum.REGULAR

    @property
    def balance_currency(self) -> 'WalletBalanceCurrenciesEnum':
        return self._regular_balance_currency

    @property
    def balance(self) -> dict[str, Decimal]:
        return self._balance

    @balance_currency.setter
    def balance_currency(self, value: 'WalletBalanceCurrenciesEnum') -> None:
        self._regular_balance_currency = value

    def __repr__(self) -> str:
        return f'{super().__repr__()}\nBalance: {self._balance}'

    __str__ = __repr__


@dataclass
class ForeignWallet(WalletBase):
    """Класс для хранения данных валютного кошелька"""

    _foreign_balance_currencies: list['WalletBalanceCurrenciesEnum']

    def __post_init__(self) -> None:
        super().__post_init__()

        DomainInvariant.no_none('foreign_balance_currencies', self._foreign_balance_currencies)

        self._balance: dict[str, Decimal] = {el.name: Decimal('0.00') for el in self._foreign_balance_currencies}
        self._status = WalletTypesEnum.FOREIGN

    @property
    def foreign_balance_currencies(self) -> list['WalletBalanceCurrenciesEnum']:
        return self._foreign_balance_currencies

    @property
    def balance(self) -> dict[str, Decimal]:
        return self._balance

    @foreign_balance_currencies.setter
    def foreign_balance_currencies(self, value: list['WalletBalanceCurrenciesEnum']) -> None:
        self._foreign_balance_currencies = value

    def __repr__(self) -> str:
        return f'{super().__repr__()}\nBalance: {self._balance}'

    __str__ = __repr__