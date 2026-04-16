class BalanceServiceFacade:
    """Класс фасад для взаимодействия с балансом"""

    def __init__(self, create_balance_service: 'CreateBalanceService', show_balance_service: 'ShowBalanceService', sort_balance_service: 'SortBalanceService', close_balance_service: 'CloseBalanceService') -> None:
        self._create_balance_service = create_balance_service
        self._show_balance_service = show_balance_service
        self._sort_balance_service = sort_balance_service
        self._close_balance_service = close_balance_service


class CreateBalanceService:
    """Класс сервис по созданию баланса"""


class ShowBalanceService:
    """Класс сервис по выводу информации о балансе"""


class SortBalanceService:
    """Класс сервис по сортировке баланса"""


class CloseBalanceService:
    """Класс сервис по закрытию баланса"""