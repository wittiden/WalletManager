from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, DateTime, Enum

from app.database.base import Base
from app.common.enums.transaction_enums import TransactionStatusesEnum, TransactionTypesEnum


class TransactionTable(Base):
    """Класс таблица транзакций"""

    __tablename__ = 'transactions'

    transaction_id: Mapped[str] = mapped_column(primary_key=True)
    from_address: Mapped[str] = mapped_column(String(26), nullable=False)
    to_address: Mapped[str] = mapped_column(String(26), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    operation_status: Mapped['TransactionStatusesEnum'] = mapped_column(Enum(TransactionStatusesEnum, name='transaction_status_enum'), default=TransactionStatusesEnum.UNKNOWN, nullable=False)
    operation_type: Mapped['TransactionTypesEnum'] = mapped_column(Enum(TransactionTypesEnum, name='transaction_type_enum'), default=TransactionTypesEnum.UNKNOWN, nullable=False)
    fee: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)
    from_currency: Mapped[str] = mapped_column(nullable=True)
    to_currency: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f'#{self.transaction_id} -> {self.operation_type}\nStatus: {self.operation_status}, from_address: {self.from_address}, to_address: {self.to_address}, amount: {self.amount}, completed_at: {self.completed_at}\nFee: {self.fee}, from_currency: {self.from_currency} -> to_currency: {self.to_currency}'

    __str__ = __repr__
