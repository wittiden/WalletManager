from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, DateTime, Enum

from app.database.base import Base
from app.common.enums.transaction_enums import TransactionStatusesEnum, TransactionTypesEnum
from app.common.enums.wallet_enums import WalletBalanceCurrenciesEnum


class TransactionTable(Base):
    """Класс таблица транзакций"""

    __tablename__ = 'transactions'

    transaction_id: Mapped[str] = mapped_column(primary_key=True)
    from_address: Mapped[str] = mapped_column(String(26), nullable=False)
    to_address: Mapped[str] = mapped_column(String(26), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    operation_status: Mapped['TransactionStatusesEnum'] = mapped_column(Enum(TransactionStatusesEnum), default=TransactionStatusesEnum.UNKNOWN)
    operation_type: Mapped['TransactionTypesEnum'] = mapped_column(Enum(TransactionTypesEnum), default=TransactionTypesEnum.UNKNOWN)
    fee: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)
    from_currency: Mapped['WalletBalanceCurrenciesEnum'] = mapped_column(Enum(WalletBalanceCurrenciesEnum), default=WalletBalanceCurrenciesEnum.UNKNOWN, nullable=False)
    to_currency: Mapped['WalletBalanceCurrenciesEnum'] = mapped_column(Enum(WalletBalanceCurrenciesEnum), default=WalletBalanceCurrenciesEnum.UNKNOWN, nullable=False)

    def __repr__(self) -> str:
        return f'#{self.transaction_id} -> {self.operation_type}\nStatus: {self.operation_status}, from_address: {self.from_address}, to_address: {self.to_address}, amount: {self.amount}, completed_at: {self.completed_at}\nFee: {self.fee}, from_currency: {self.from_currency} -> to_currency: {self.to_currency}'

    __str__ = __repr__
