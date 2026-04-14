from app.database.base import Base
from app.database.engine import engine
from app.database.models.user import UserTable
from app.database.models.transaction import TransactionTable
from app.database.models.wallet import WalletTable


def create_tables() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)