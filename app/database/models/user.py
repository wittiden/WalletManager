from typing import TYPE_CHECKING

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums.user_enums import UserStatusesEnum
from app.database.base import Base

if TYPE_CHECKING:
    from app.database.models.wallet import WalletTable


class UserTable(Base):
    """Класс таблица пользователей"""

    __tablename__ = 'users'

    user_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_blocked: Mapped[bool] = mapped_column(default=False, nullable=False)
    status: Mapped['UserStatusesEnum'] = mapped_column(Enum(UserStatusesEnum, name='user_status_enum'), default=UserStatusesEnum.UNKNOWN, nullable=False)

    wallets: Mapped[list['WalletTable']] = relationship('WalletTable', back_populates='owner', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'{self.status.value} #{self.user_id} (name: {self.name}, email: {self.email}, password: {self.password}, is_blocked: {self.is_blocked})'

    __str__ = __repr__
