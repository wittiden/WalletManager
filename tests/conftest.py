import datetime
from decimal import Decimal

import pytest

from app.infrastructure.balances.domain import BalanceBase, ForeignBalance, RegularBalance
from app.infrastructure.transactions.domain import DepositTransaction, ExchangeTransaction, WithdrawTransaction
from app.infrastructure.users.domain import UserBase
from app.infrastructure.wallets.domain import WalletBase


@pytest.fixture
def sample_user_base():
    return UserBase('test', 'test@gmail.com', 'pass123')


@pytest.fixture
def sample_wallet_base():
    return WalletBase('1234', 'owner_id')


@pytest.fixture
def sample_balance_base():
    return BalanceBase('wallet_id')


@pytest.fixture
def sample_balance_regular():
    return RegularBalance('wallet_id', Decimal(1), 'BYN')


@pytest.fixture
def sample_balance_foreign():
    return ForeignBalance('wallet_id', [Decimal(1), Decimal(9.07), Decimal(0.5)], ['BYN', 'RUB', 'USD'])


@pytest.fixture
def sample_transaction_deposit():
    return DepositTransaction('12345', '54321', datetime.datetime.now(), Decimal(1), Decimal(0), 'USD')


@pytest.fixture
def sample_transaction_withdraw():
    return WithdrawTransaction('12345', '54321', datetime.datetime.now(), Decimal(1), Decimal(0.03), 'BYN')


@pytest.fixture
def sample_transaction_exchange():
    return ExchangeTransaction('12345', '54321', datetime.datetime.now(), Decimal(1), Decimal(0.03), 'USD', 'BYN', Decimal(13.6))
