from typing import TYPE_CHECKING
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from app.wallets.domain import WalletBase


class WalletCommandsRepository:
    """Класс репозиторий crud операций кошелька"""

    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def insert_wallet_info(self, wallet: 'WalletBase') -> None:
        pass

    def update_wallet_info(self, wallet: 'WalletBase', new_wallet_data) -> None:
        pass

    def delete_wallet_info(self, wallet: 'WalletBase') -> None:
        pass