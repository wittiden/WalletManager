from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric, Enum

from app.common.enums.balance_enums import BalanceTypesEnum
from app.database.base import Base

if TYPE_CHECKING:
    from app.database.models.wallet import WalletTable


class BalanceTable(Base):
    """Класс таблица балансов"""

    __tablename__ = 'balances'

    balance_id: Mapped[str] = mapped_column(primary_key=True)
    wallet_id: Mapped[str] = mapped_column(ForeignKey('wallets.wallet_id'), nullable=False)
    is_frozen: Mapped[bool] = mapped_column(default=False, nullable=False)
    currency: Mapped[str] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    balance_type: Mapped['BalanceTypesEnum'] = mapped_column(Enum(BalanceTypesEnum, name='balance_type_enum'), default=BalanceTypesEnum.UNKNOWN, nullable=False)

    wallet: Mapped['WalletTable'] = relationship('WalletTable', back_populates='balance')

    def __repr__(self) -> str:
        return f'{self.balance_type} #{self.balance_id} -> wallet_id: #{self.wallet_id}\nIs_frozen: {self.is_frozen}'

    __str__ = __repr__
