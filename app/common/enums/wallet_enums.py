from enum import Enum


class WalletTypesEnum(Enum):
    """Енам класс для перечисления типов кошельков"""

    UNKNOWN = 'Неизвестный тип счета'
    DEBIT = 'Дебетовый счет'
    CREDIT = 'Кредитный счет'
