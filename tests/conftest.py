import pytest

from app.infrastructure.users.domain import UserBase
from app.infrastructure.wallets.domain import WalletBase


@pytest.fixture
def sample_user_base():
    return UserBase('test', 'test@gmail.com', 'pass123')

@pytest.fixture
def sample_wallet_base():
    return WalletBase('1234', 'owner_id')