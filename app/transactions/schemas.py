from decimal import Decimal
from pydantic import BaseModel, field_validator, Field

from app.common.enums.transaction_enums import TransactionStatusesEnum, TransactionTypesEnum
from app.core.exceptions import AddressFormatError


def validate_address(address: str) -> str:
    if len(address) != 26:
        raise AddressFormatError('Address length != 26')

    return address


class CreateDepositTransactionSchema(BaseModel):
    """Класс схема для проверки полей при создании debit транзакции"""

    from_address: str
    to_address: str
    amount: Decimal = Field(gt=0)
    operation_status: TransactionStatusesEnum
    operation_type: TransactionTypesEnum

    @field_validator('from_address', 'to_address')
    @classmethod
    def validate_address(cls, address: str) -> str:
        return validate_address(address)


class CreateWithdrawTransactionSchema(BaseModel):
    """Класс схема для проверки полей при создании withdraw транзакции"""

    from_address: str
    to_address: str
    amount: Decimal = Field(gt=0)
    operation_status: TransactionStatusesEnum
    operation_type: TransactionTypesEnum
    withdraw_fee: Decimal = Field(gt=0)

    @field_validator('from_address', 'to_address')
    @classmethod
    def validate_address(cls, address: str) -> str:
        return validate_address(address)


class CreateExchangeTransactionSchema(BaseModel):
    """Класс схема для проверки полей при создании exchange транзакции"""

    from_address: str
    to_address: str
    amount: Decimal = Field(gt=0)
    operation_status: TransactionStatusesEnum
    operation_type: TransactionTypesEnum
    exchange_fee: Decimal = Field(gt=0)
    from_currency: str
    to_currency: str

    @field_validator('from_address', 'to_address')
    @classmethod
    def validate_address(cls, address: str) -> str:
        return validate_address(address)