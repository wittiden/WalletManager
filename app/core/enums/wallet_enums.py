from enum import Enum


class WalletTypesEnum(Enum):
    """Енам класс для перечисления типов кошельков"""

    UNKNOWN = 'Неизвестный тип'
    REGULAR = 'Обычный кошелек'
    FOREIGN = 'Валютный кошелек'


class WalletStrategyTypesEnum(Enum):
    """"""

    UNKNOWN = 'Неизвестный тип'
    DEBIT = 'Дебетовая стратегия'
    CREDIT = 'Кредитная стратегия'


class WalletBalanceCurrenciesEnum(Enum):
    """Енам класс для перечисления типов валют (идет динамическая запись runtime)"""

    UNKNOWN = 'Неизвестный тип валюты'
