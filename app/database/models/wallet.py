from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum

from app.database.base import Base
from app.common.enums.wallet_enums import WalletTypesEnum

if TYPE_CHECKING:
    from app.database.models.user import UserTable
    from app.database.models.balance import BalanceTable


class WalletTable(Base):
    """Класс таблица кошельков"""

    __tablename__ = 'wallets'

    wallet_id: Mapped[str] = mapped_column(primary_key=True)
    pin: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False, unique=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    account_type: Mapped[WalletTypesEnum] = mapped_column(Enum(WalletTypesEnum, name='wallet_type_enum'), default=WalletTypesEnum.UNKNOWN, nullable=False)

    owner: Mapped['UserTable'] = relationship('UserTable', back_populates='wallets')
    balance: Mapped[list['BalanceTable']] = relationship('BalanceTable', back_populates='wallet', cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f'{self.account_type.value} #{self.wallet_id} -> owner_id #{self.owner_id} (pin: {self.pin}, address: {self.address}, is_blocked: {self.is_blocked})'

    __str__ = __repr__
