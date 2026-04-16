from typing import TYPE_CHECKING, ParamSpec

from app.common.enums.balance_enums import BalanceTypesEnum
from app.core.validations import GeneralValidation

if TYPE_CHECKING:
    from app.balances.domain import BalanceBase

P = ParamSpec('P')


class BalanceRegistry:
    """Класс для регистрации типов балансов"""

    def __init__(self) -> None:
        self._registrations: dict['BalanceTypesEnum', type['BalanceBase']] = {}

    def set_registration(self, key: 'BalanceTypesEnum', value: type['BalanceBase']) -> None:
        self._registrations[key] = value

    def get_registration(self, key: 'BalanceTypesEnum') -> type['BalanceBase']:
        return GeneralValidation.not_none_checker(self._registrations.get(key))

    def get_all_registrations(self) -> dict['BalanceTypesEnum', type['BalanceBase']]:
        return self._registrations


class BalanceFactory:
    """Класс фабрика по созданию балансов"""

    def __init__(self, registry: 'BalanceRegistry') -> None:
        self._registry = registry

    def create_balance(self, key: 'BalanceTypesEnum', *args: P.args, **kwargs: P.kwargs) -> 'BalanceBase':
        class_type = self._registry.get_registration(key)
        return class_type(*args, **kwargs)
