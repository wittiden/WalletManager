from typing import TYPE_CHECKING
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from app.users.domain import UserBase


class WalletQueriesRepository:
    """Класс репозиторий select операций кошелька"""

    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def select_for_close(self, find_wallet_id: str, pin: str):
        pass

    def select_all_wallets(self):
        pass

    def select_my_wallets(self, user: 'UserBase'):
        pass

    def select_wallet(self, find_wallet_id: str):
        pass

    def select_order_by_wallets(self, order_by_param: str):
        pass

    def select_order_by_my_wallets(self, user: 'UserBase', order_by_param: str):
        pass