from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum

from app.database.base import Base
from app.common.enums.wallet_enums import WalletTypesEnum, WalletBalanceCurrenciesEnum, WalletStrategyTypesEnum

if TYPE_CHECKING:
    from app.database.models.user import UserTable


class WalletTable(Base):
    """Класс таблица кошельков"""

    __tablename__ = 'wallets'

    wallet_id: Mapped[str] = mapped_column(primary_key=True)
    pin: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    status: Mapped[WalletTypesEnum] = mapped_column(Enum(WalletTypesEnum), default=WalletTypesEnum.UNKNOWN)

    owner: Mapped['UserTable'] = relationship('UserTable', back_populates='wallets')

