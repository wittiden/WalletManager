from enum import Enum


class TransactionStatusesEnum(Enum):
    """Енам класс для перечисления статусов транзакций"""

    UNKNOWN = 'Состояние транзакции неизвестно'
    PENDING = 'Транзакция в процессе'
    SUCCESS = 'Транзакция успешно завершена'
    FAILED = 'Транзакция отклонена'


class TransactionTypesEnum(Enum):
    """Енам класс для перечисления типов транзакций"""

    UNKNOWN = 'Транзакция неизвестного типа'
    DEPOSIT = 'Транзакция пополнения'
    WITHDRAW = 'Транзакция снятия'
    EXCHANGE = 'Транзакция обмена'