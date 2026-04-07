from dataclasses import dataclass, field
from typing import Any

from app.core.enums.user_enums import UserStatusesEnum
from app.core.utils.general_funcs import get_hash
from app.core.utils.mixins import MixinId


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
        self._name = value

    @email.setter
    def email(self, value: str) -> None:
        self._email = value

    @password.setter
    def password(self, value: str) -> None:
        self._password = value
        self._password = get_hash(self._password)

    @is_blocked.setter
    def is_blocked(self, value: bool) -> None:
        self._is_blocked = value

    def __repr__(self) -> str:
        return f'{self._status.value} #{self.item_id}\nName: {self._name}, email: {self._email}, password: {self._password}, is_blocked: {self._is_blocked}'

    def __str__(self) -> str:
        return f'{self._status.value} #{self.item_id}\nName: {self._name}, email: {self._email}, password: {self._password}, is_blocked: {self._is_blocked}'


@dataclass
class Client(UserBase):
    """Датакласс для хранения данных клиента"""

    _wallets: list[Any] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        self._status = UserStatusesEnum.CLIENT

    @property
    def wallets(self) -> list[Any]:
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