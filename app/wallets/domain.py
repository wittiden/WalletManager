import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from typing import TYPE_CHECKING, ParamSpec
from blinker import Signal

from app.core.enums.wallet_enums import WalletBalanceCurrenciesEnum
from app.core.enums.wallet_enums import WalletTypesEnum
from app.core.utils.general_funcs import get_hash, blink_func
from app.core.utils.mixins import MixinId
from app.core.validations.wallet_validations import WalletBaseValidation

if TYPE_CHECKING:
    from app.users.domain import UserBase
    from app.wallets.strategy import WalletStrategy

P = ParamSpec('P')

wallet_upgrade_signal = Signal()
wallet_upgrade_signal.connect(blink_func)


@dataclass
class WalletBase(MixinId):
    """Базовый класс для хранения данных кошелька"""

    _pin: str
    _is_blocked: bool = field(default=False, init=False)
    _owner: 'UserBase' = field(default=None, init=False)
    _status: 'WalletTypesEnum' = field(default=WalletTypesEnum.UNKNOWN, init=False)

    def __post_init__(self) -> None:
        super().__init__()

        WalletBaseValidation.valid_pin(self._pin)

        self._address: str = uuid.uuid4().hex[:16]

        self._pin = get_hash(self._pin)

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
        WalletBaseValidation.valid_pin(value)
        self._pin = get_hash(value)

    @is_blocked.setter
    def is_blocked(self, value: 'bool') -> None:
        old_value = self._is_blocked
        WalletBaseValidation.valid_is_blocked(value)
        self._is_blocked = value
        wallet_upgrade_signal.send(self, field='is_blocked', old=old_value, new=value)

    @owner.setter
    def owner(self, value: 'UserBase') -> None:
        old_value = self._owner
        WalletBaseValidation.valid_owner(value)
        self._owner = value
        wallet_upgrade_signal.send(self, field='owner', old=old_value, new=value)

    def __repr__(self) -> str:
        return f'{self.status.value} #{self.item_id} - owner: {self._owner.status if self._owner else 'кошелек не имеет привязки'} #{self._owner.item_id if self._owner else 'None'}\nAddress: {self._address}, is_blocked: {self._is_blocked}'

    __str__ = __repr__


@dataclass
class RegularWallet(WalletBase):
    """Класс для хранения данных обычного кошелька"""

    _regular_balance_currency: 'WalletBalanceCurrenciesEnum'
    _strategy: 'WalletStrategy'

    def __post_init__(self) -> None:
        super().__post_init__()

        WalletBaseValidation.valid_strategy(self._strategy)
        WalletBaseValidation.valid_regular_balance_currency(self._regular_balance_currency)

        self._balance: dict[str, Decimal] = {self._regular_balance_currency.name: Decimal('0.00')}
        self._status = WalletTypesEnum.REGULAR

    @property
    def balance_currency(self) -> 'WalletBalanceCurrenciesEnum':
        return self._regular_balance_currency

    @property
    def balance(self) -> dict[str, Decimal]:
        return self._balance

    @property
    def strategy(self) -> 'WalletStrategy':
        return self._strategy

    @strategy.setter
    def strategy(self, value: 'WalletStrategy') -> None:
        old_value = self._strategy
        WalletBaseValidation.valid_strategy(value)
        self._strategy = value
        wallet_upgrade_signal.send(self, field='strategy', old=old_value, new=value)

    def __repr__(self) -> str:
        return f'{super().__repr__()}\nStrategy: {type(self._strategy).__name__}\nBalance: {self._balance}'

    __str__ = __repr__


@dataclass
class ForeignWallet(WalletBase):
    """Класс для хранения данных валютного кошелька"""

    _foreign_balance_currencies: list['WalletBalanceCurrenciesEnum']

    def __post_init__(self) -> None:
        super().__post_init__()

        WalletBaseValidation.valid_foreign_balance_currencies(self._foreign_balance_currencies)

        self._balance: dict[str, Decimal] = {el.name: Decimal('0.00') for el in self._foreign_balance_currencies}
        self._status = WalletTypesEnum.FOREIGN

    @property
    def balance(self) -> dict[str, Decimal]:
        return self._balance

    def __repr__(self) -> str:
        return f'{super().__repr__()}\nBalance: {self._balance}'

    __str__ = __repr__