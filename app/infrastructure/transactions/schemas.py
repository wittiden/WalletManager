from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.common.enums.transaction_enums import TransactionTypesEnum
from app.core.exceptions import AddressFormatError


def validate_address(address: str) -> str:
    if len(address) != 26:
        raise AddressFormatError('Address length != 26')

    return address


class CreateDepositOrWithdrawTransactionSchema(BaseModel):
    """Класс схема для проверки полей при создании транзакций пополнения и снятия"""

    currency: str
    from_address: str
    to_address: str
    amount: Decimal = Field(gt=0)
    fee: Decimal = Field(ge=0)
    operation_type: TransactionTypesEnum

    @field_validator('from_address', 'to_address')
    @classmethod
    def validate_address(cls, address: str) -> str:
        return validate_address(address)


class CreateExchangeTransactionSchema(BaseModel):
    """Класс схема для проверки полей при создании exchange транзакции"""

    from_address: str
    to_address: str
    amount: Decimal = Field(gt=0)
    fee: Decimal = Field(gt=0)
    operation_type: TransactionTypesEnum
    from_currency: str
    to_currency: str
    rate: Decimal = Field(gt=0)

    @field_validator('from_address', 'to_address')
    @classmethod
    def validate_address(cls, address: str) -> str:
        return validate_address(address)
