from pydantic import BaseModel, field_validator

from app.core.enums.wallet_enums import WalletBalanceCurrenciesEnum, WalletTypesEnum
from app.core.validations.exceptions import PinFormatError
from app.wallets.strategy import WalletStrategy


def validate_pin(pin: str) -> str:
    if len(pin) != 4:
        raise PinFormatError('Pin length != 4')

    if not all(letter.isdigit() for letter in pin):
        raise PinFormatError('Pin must contain only digits')

    return pin.strip()


class CreateRegularWalletSchema(BaseModel):
    """Класс схема для проверки полей при создании обычного кошелька"""

    key: WalletTypesEnum
    pin: str
    balance_currency: WalletBalanceCurrenciesEnum

    @field_validator('pin')
    @classmethod
    def validate_pin(cls, pin: str) -> str:
        return validate_pin(pin)


class CreateForeignWalletSchema(BaseModel):
    """Класс схема для проверки полей при создании валютного кошелька"""

    key: WalletTypesEnum
    pin: str
    balance_currency: list[WalletBalanceCurrenciesEnum]

    @field_validator('pin')
    @classmethod
    def validate_pin(cls, pin: str) -> str:
        return validate_pin(pin)


class CloseWalletSchema(BaseModel):
    """Класс схема для проверки полей при закрытии кошелька"""

    wallet_id: str
    pin: str

    @field_validator('pin')
    @classmethod
    def validate_pin(cls, pin: str) -> str:
        return validate_pin(pin)