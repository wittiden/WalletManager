from enum import Enum


class WalletTypesEnum(Enum):
    """Енам класс для перечисления типов кошельков"""

    UNKNOWN = 'Неизвестный тип'
    REGULAR = 'Обычный кошелек'
    FOREIGN = 'Валютный кошелек'


class WalletBalanceCurrenciesEnum(Enum):
    """Енам класс для перечисления типов валют (идет динамическая запись runtime)"""

    UNKNOWN = 'Неизвестный тип валюты'
