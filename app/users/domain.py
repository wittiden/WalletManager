from dataclasses import dataclass, field
from blinker import Signal

from app.common.enums.user_enums import UserStatusesEnum
from app.common.mixins import MixinId
from app.core.invariants import DomainInvariant
from app.core.utils import blink_func

user_upgrade_signal = Signal()
user_upgrade_signal.connect(blink_func)


@dataclass
class UserBase(MixinId):
    """Датакласс для хранения данных пользователя"""

    _name: str
    _email: str
    _password: str
    _is_blocked: bool = field(default=False)
    _status: 'UserStatusesEnum' = field(default=UserStatusesEnum.UNKNOWN, init=False)

    def __post_init__(self) -> None:
        super().__init__()

        DomainInvariant.no_empty('name', self._name)
        DomainInvariant.no_empty('email', self._email)
        DomainInvariant.no_empty('password', self._password)

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
        self._name = DomainInvariant.no_empty('name', value)
        user_upgrade_signal.send(self, field='name', old=old_value, new=value)

    @email.setter
    def email(self, value: str) -> None:
        old_value = self._email
        self._email = DomainInvariant.no_empty('email', value)
        user_upgrade_signal.send(self, field='email', old=old_value, new=value)

    @password.setter
    def password(self, value: str) -> None:
        self._password = DomainInvariant.no_empty('password', value)

    @is_blocked.setter
    def is_blocked(self, value: bool) -> None:
        old_value = self._is_blocked
        self._is_blocked = DomainInvariant.is_instance('is_blocked', value, bool)
        user_upgrade_signal.send(self, field='is_blocked', old=old_value, new=value)

    def __repr__(self) -> str:
        return f'{self._status.value} #{self.item_id}\nName: {self._name}, email: {self._email}, is_blocked: {self._is_blocked}'

    __str__ = __repr__


@dataclass
class Client(UserBase):
    """Датакласс для хранения данных клиента"""

    def __post_init__(self) -> None:
        super().__post_init__()

        self._status = UserStatusesEnum.CLIENT

    def __repr__(self) -> str:
        return f'{super().__repr__()}\n'

    __str__ = __repr__


@dataclass
class Admin(UserBase):
    """Датакласс для хранения данных администратора"""

    def __post_init__(self) -> None:
        super().__post_init__()

        self._status = UserStatusesEnum.ADMIN

    def __repr__(self) -> str:
        return f'{super().__repr__()}\n'

    __str__ = __repr__