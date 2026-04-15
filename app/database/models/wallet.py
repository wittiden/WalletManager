from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum, Numeric

from app.database.base import Base
from app.common.enums.wallet_enums import WalletTypesEnum, WalletBalanceCurrenciesEnum

if TYPE_CHECKING:
    from app.database.models.user import UserTable


class WalletTable(Base):
    """Класс таблица кошельков"""

    __tablename__ = 'wallets'

    wallet_id: Mapped[str] = mapped_column(primary_key=True)
    pin: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False, unique=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    status: Mapped[WalletTypesEnum] = mapped_column(Enum(WalletTypesEnum, name='wallet_type_enum'), default=WalletTypesEnum.UNKNOWN, nullable=False)

    owner: Mapped['UserTable'] = relationship('UserTable', back_populates='wallets')
    balance: Mapped[list['BalanceTable']] = relationship('BalanceTable', back_populates='wallet', cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f'{self.status.value} #{self.wallet_id} - owner: {self.owner.status} #{self.owner.user_id}\nAddress: {self.address}, is_blocked: {self.is_blocked}'

    __str__ = __repr__


class BalanceTable(Base):
    """Класс таблица балансов"""

    __tablename__ = 'balances'

    wallet_id: Mapped[str] = mapped_column(ForeignKey('wallets.wallet_id'), primary_key=True)
    balance_currency: Mapped['WalletBalanceCurrenciesEnum'] = mapped_column(Enum(WalletBalanceCurrenciesEnum), primary_key=True)
    balance_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    wallet: Mapped['WalletTable'] = relationship('WalletTable', back_populates='balance')

    def __repr__(self) -> str:
        return f'#{self.wallet_id}\n{self.balance_currency}: {self.balance_amount}'

    __str__ = __repr__

