import uuid
from dataclasses import dataclass, field
from blinker import Signal

from app.common.enums.wallet_enums import WalletTypesEnum
from app.common.mixins import MixinId
from app.core.invariants import DomainInvariant
from app.core.utils import blink_func


wallet_upgrade_signal = Signal()
wallet_upgrade_signal.connect(blink_func)


@dataclass
class WalletBase(MixinId):
    """Базовый класс для хранения данных счета"""

    _pin: str
    _owner_id: str
    _address: str = field(default_factory=lambda: uuid.uuid4().hex[:26], init=False)
    _is_blocked: bool = field(default=False, init=False)
    _account_type: 'WalletTypesEnum' = field(default=WalletTypesEnum.UNKNOWN, init=False)

    def __post_init__(self) -> None:
        super().__init__()

        DomainInvariant.no_empty('pin', self._pin)
        DomainInvariant.no_empty('owner_id', self._owner_id)
        DomainInvariant.no_empty('address', self._address)

    @property
    def pin(self) -> str:
        return self._pin

    @property
    def account_type(self) -> 'WalletTypesEnum':
        return self._account_type

    @property
    def is_blocked(self) -> bool:
        return self._is_blocked

    @property
    def owner_id(self) -> 'str':
        return self._owner_id

    @property
    def address(self) -> str:
        return self._address

    @pin.setter
    def pin(self, value: str) -> None:
        self._pin = DomainInvariant.no_empty('pin', value)

    @address.setter
    def address(self, value: str) -> None:
        self._address = value

    @owner_id.setter
    def owner_id(self, value: str) -> None:
        old_value = self._owner_id
        self._owner_id = DomainInvariant.no_none('owner', value)
        wallet_upgrade_signal.send(self, field='owner', old=old_value, new=value)

    @is_blocked.setter
    def is_blocked(self, value: 'bool') -> None:
        old_value = self._is_blocked
        self._is_blocked = DomainInvariant.is_instance('is_blocked', value, bool)
        wallet_upgrade_signal.send(self, field='is_blocked', old=old_value, new=value)

    def __repr__(self) -> str:
        return f'{self.account_type.value} #{self.item_id} - owner_id: #{self.owner_id}\nAddress: {self._address}, is_blocked: {self._is_blocked}'

    __str__ = __repr__


@dataclass
class CreditWallet(WalletBase):
    """Класс для хранения данных кредитного счета"""

    def __post_init__(self) -> None:
        super().__post_init__()

        self._account_type = WalletTypesEnum.CREDIT

    def __repr__(self) -> str:
        return f'{super().__repr__()}'

    __str__ = __repr__


@dataclass
class DebitWallet(WalletBase):
    """Класс для хранения дебетового счета"""

    def __post_init__(self) -> None:
        super().__post_init__()

        self._account_type = WalletTypesEnum.DEBIT

    def __repr__(self) -> str:
        return f'{super().__repr__()}'

    __str__ = __repr__