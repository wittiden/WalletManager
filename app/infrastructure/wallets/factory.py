from typing import ParamSpec, TYPE_CHECKING

from app.common.enums.wallet_enums import WalletTypesEnum
from app.core.validations import GeneralValidation

if TYPE_CHECKING:
    from app.infrastructure.wallets.domain import WalletBase

P = ParamSpec('P')


class WalletFactoryRegistry:
    """Класс регистрирующий типы данных кошельков для работы фабрики"""

    def __init__(self) -> None:
        self._registrations: dict['WalletTypesEnum', type['WalletBase']] = {}

    def set_registration(self, key: 'WalletTypesEnum', value: type['WalletBase']) -> None:
        self._registrations[key] = value

    def get_registration(self, key: 'WalletTypesEnum') -> type['WalletBase']:
        return GeneralValidation.not_none_checker(self._registrations.get(key))

    def get_all_registrations(self) -> dict['WalletTypesEnum', type['WalletBase']]:
        return self._registrations


class WalletFactory:
    """Класс фабрика по созданию кошельков разных типов"""

    def __init__(self, wallet_factory_registry: 'WalletFactoryRegistry') -> None:
        self._wallet_factory_registry = wallet_factory_registry

    def create_wallet(self, key: 'WalletTypesEnum', *args: P.args, **kwargs: P.kwargs) -> 'WalletBase':
        class_type = self._wallet_factory_registry.get_registration(key)
        return class_type(*args, **kwargs)