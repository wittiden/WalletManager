from datetime import datetime
from pydantic import BaseModel, field_validator

from app.common.enums.transaction_enums import TransactionStatusesEnum, TransactionTypesEnum
from app.core.exceptions import AddressFormatError


class CreateTransactionScheme(BaseModel):
    from_address: str
    to_address: str
    completed_at: datetime
    operation_status: TransactionStatusesEnum
    operation_type: TransactionTypesEnum

    @field_validator('from_address', 'to_address')
    @classmethod
    def validate_address(cls, address: str) -> str:
        if len(address) != 26:
            raise AddressFormatError('Address length != 26')

        return address