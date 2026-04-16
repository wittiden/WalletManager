from enum import Enum


class BalanceTypesEnum(Enum):
    """Енам класс для перечисления типов балансов"""

    UNKNOWN = 'Баланс неизвестного типа'
    REGULAR = 'Обычный баланс'
    FOREIGN = 'Валютный баланс'


class WalletBalanceCurrenciesEnum(Enum):
    """Енам класс для перечисления типов валют (идет динамическая запись runtime)"""

    UNKNOWN = 'Неизвестный тип валюты'