from app.core.enums.wallet_enums import WalletBalanceCurrenciesEnum
from app.core.validations.exceptions import IsInstanceError, PinFormatError
from app.core.validations.general_validations import GeneralValidation
from app.users.domain import UserBase


class WalletBaseValidation:
    """Класс для валидирования атрибутов кошелька"""

    @staticmethod
    def valid_pin(pin: str) -> str:
        GeneralValidation.isinstance_checker(pin, str)

        GeneralValidation.not_empty_checker(pin)

        if len(pin) != 4:
            raise PinFormatError(f'{pin} length != 4')

        if not all(letter.isdigit() for letter in pin):
            raise PinFormatError(f'all {pin} letters != digits')

        return pin

    @staticmethod
    def valid_is_blocked(is_blocked: bool) -> bool:
        GeneralValidation.isinstance_checker(is_blocked, bool)

        return is_blocked

    @staticmethod
    def valid_owner(owner: 'UserBase') -> 'UserBase':
        GeneralValidation.isinstance_checker(owner, UserBase)

        return owner

    @staticmethod
    def valid_regular_balance_currency(regular_balance_currency: 'WalletBalanceCurrenciesEnum') -> 'WalletBalanceCurrenciesEnum':
        GeneralValidation.isinstance_checker(regular_balance_currency, WalletBalanceCurrenciesEnum)

        return regular_balance_currency

    @staticmethod
    def valid_foreign_balance_currencies(foreign_balance_currencies: list['WalletBalanceCurrenciesEnum']) -> list['WalletBalanceCurrenciesEnum']:
        GeneralValidation.isinstance_checker(foreign_balance_currencies, list)

        if not all(isinstance(currency, WalletBalanceCurrenciesEnum) for currency in foreign_balance_currencies):
            raise IsInstanceError('currency must be WalletBalanceCurrenciesEnum')

        return foreign_balance_currencies