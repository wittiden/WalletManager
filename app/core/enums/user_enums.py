from enum import Enum


class UserStatusesEnum(Enum):
    """Енам класс для хранения статуса пользователя"""

    UNKNOWN = 'Неизвестный пользователь'
    CLIENT = 'Клиент'
    ADMIN = 'Администратор'
