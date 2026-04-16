from typing import TYPE_CHECKING, Any
from sqlalchemy.orm import sessionmaker

from app.database.models import WalletTable

if TYPE_CHECKING:
    from app.infrastructure.wallets.domain import WalletBase
    from app.infrastructure.wallets.repository.mapper import WalletMapper


class WalletCommandsRepository:
    """Класс репозиторий crud операций кошельков"""

    def __init__(self, session_factory: sessionmaker, wallet_mapper: 'WalletMapper') -> None:
        self._session_factory = session_factory
        self._wallet_mapper = wallet_mapper

    def insert_wallet_info(self, wallet: 'WalletBase') -> None:
        with self._session_factory() as session:
            session.add(self._wallet_mapper.domain_to_table(wallet))
            session.commit()

    def delete_wallet_info(self, wallet: 'WalletBase') -> None:
        with self._session_factory() as session:
            obj = session.get(WalletTable, wallet.item_id)
            if obj:
                session.delete(obj)
                session.commit()

    def update_wallet_info(self, wallet: 'WalletBase', new_wallet_params: dict[str, Any]) -> None:
        with self._session_factory() as session:
            obj = session.get(WalletTable, wallet.item_id)
            if obj:
                for key, value in new_wallet_params.items():
                    setattr(obj, key, value)

                session.commit()