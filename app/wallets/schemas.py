from pydantic import BaseModel, field_validator, Field

from app.common.enums.wallet_enums import WalletTypesEnum
from app.core.exceptions import PinFormatError


def validate_pin(pin: str) -> str:
    if len(pin) != 4:
        raise PinFormatError('Pin length != 4')

    if not all(letter.isdigit() for letter in pin):
        raise PinFormatError('Pin must contain only digits')

    return pin.strip()


class CreateWalletSchema(BaseModel):
    """Класс схема для проверки полей при создании кошелька"""

    key: WalletTypesEnum
    pin: str

    @field_validator('pin')
    @classmethod
    def validate_pin(cls, pin: str) -> str:
        return validate_pin(pin)


class CloseWalletSchema(BaseModel):
    """Класс схема для проверки полей при закрытии кошелька"""

    pin: str
    address: str = Field(max_length=26, min_length=26)

    @field_validator('pin')
    @classmethod
    def validate_pin(cls, pin: str) -> str:
        return validate_pin(pin)

