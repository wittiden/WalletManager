from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from blinker import Signal

from app.core.enums.user_enums import UserStatusesEnum
from app.core.utils.general_funcs import get_hash, blink_func
from app.core.utils.mixins import MixinId
from app.core.validations.user_validations import UserBaseValidation

if TYPE_CHECKING:
    from app.wallets.domain import WalletBase

user_name_signal = Signal()
user_email_signal = Signal()
user_password_signal = Signal()
user_is_blocked_signal = Signal()
user_wallets_signal = Signal()

user_name_signal.connect(blink_func)
user_email_signal.connect(blink_func)
user_password_signal.connect(blink_func)
user_is_blocked_signal.connect(blink_func)
user_wallets_signal.connect(blink_func)


@dataclass
class UserBase(MixinId):
    """Датакласс для хранения данных пользователя"""

    _name: str
    _email: str
    _password: str
    _is_blocked: bool = field(default=False, init=False)
    _status: 'UserStatusesEnum' = field(default=UserStatusesEnum.UNKNOWN, init=False)

    def __post_init__(self) -> None:
        super().__init__()

        UserBaseValidation.valid_name(self._name)
        UserBaseValidation.valid_email(self._email)
        UserBaseValidation.valid_password(self._password)

        self._password = get_hash(self._password)

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def password(self) -> str:
        return self._password

    @property
    def is_blocked(self) -> bool:
        return self._is_blocked

    @property
    def status(self) -> 'UserStatusesEnum':
        return self._status

    @name.setter
    def name(self, value: str) -> None:
        old_value = self._name
        self._name = UserBaseValidation.valid_name(value)
        user_name_signal.send(self, data=[old_value, value])

    @email.setter
    def email(self, value: str) -> None:
        old_value = self._email
        self._email = UserBaseValidation.valid_email(value)
        user_email_signal.send(self, data=[old_value, value])

    @password.setter
    def password(self, value: str) -> None:
        old_value = self._password
        self._password = UserBaseValidation.valid_password(value)
        self._password = get_hash(self._password)
        user_password_signal.send(self, data=[old_value, value])

    @is_blocked.setter
    def is_blocked(self, value: bool) -> None:
        old_value = self._is_blocked
        self._is_blocked = UserBaseValidation.valid_is_blocked(value)
        user_is_blocked_signal.send(self, data=[old_value, value])

    def __repr__(self) -> str:
        return f'{self._status.value} #{self.item_id}\nName: {self._name}, email: {self._email}, password: {self._password}, is_blocked: {self._is_blocked}'

    def __str__(self) -> str:
        return f'{self._status.value} #{self.item_id}\nName: {self._name}, email: {self._email}, password: {self._password}, is_blocked: {self._is_blocked}'


@dataclass
class Client(UserBase):
    """Датакласс для хранения данных клиента"""

    _wallets: list['WalletBase'] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        self._status = UserStatusesEnum.CLIENT

    @property
    def wallets(self) -> list['WalletBase']:
        return self._wallets

    def __repr__(self) -> str:
        return f'{super().__repr__()}\nWallets:\n{[f'{wallet}\n' for wallet in self._wallets]}\n'

    def __str__(self) -> str:
        return f'{super().__str__()}\nWallets:\n{[f'{wallet}\n' for wallet in self._wallets]}\n'


@dataclass
class Admin(UserBase):
    """Датакласс для хранения данных администратора"""

    def __post_init__(self) -> None:
        super().__post_init__()

        self._status = UserStatusesEnum.ADMIN

    def __repr__(self) -> str:
        return f'{super().__repr__()}\n'

    def __str__(self) -> str:
        return f'{super().__str__()}\n'