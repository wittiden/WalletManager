from typing import TYPE_CHECKING, ParamSpec

from app.common.enums.transaction_enums import TransactionTypesEnum
from app.core.validations import GeneralValidation

if TYPE_CHECKING:
    from app.infrastructure.transactions.domain import TransactionBase

P = ParamSpec('P')


class TransactionRegistry:
    """Класс для регистрации типов транзакций"""

    def __init__(self) -> None:
        self._registrations: dict['TransactionTypesEnum', type['TransactionBase']] = {}

    def get_registration(self, key: 'TransactionTypesEnum') -> type['TransactionBase']:
        return GeneralValidation.not_none_checker(self._registrations.get(key))

    def get_all_registrations(self) -> dict['TransactionTypesEnum', type['TransactionBase']]:
        return self._registrations

    def set_registration(self, key: 'TransactionTypesEnum', value: type['TransactionBase']) -> None:
        self._registrations[key] = value


class TransactionFactory:
    """Класс фабрика для создания транзакции любого типа"""

    def __init__(self, registry: 'TransactionRegistry') -> None:
        self._registry = registry

    def create_transaction(self, key: 'TransactionTypesEnum', *args: P.args, **kwargs: P.kwargs) -> 'TransactionBase':
        transaction_type = self._registry.get_registration(key)
        return transaction_type(*args, **kwargs)
