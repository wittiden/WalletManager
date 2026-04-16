from typing import TYPE_CHECKING, Any
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from app.infrastructure.balances.repository.mapper import BalanceMapper


class BalanceQueriesRepository:
    """Класс репозиторий select операций баланса"""

    def __init__(self, session_factory: sessionmaker, balance_mapper: 'BalanceMapper') -> None:
        self._session_factory = session_factory
        self._balance_mapper = balance_mapper
