from decimal import Decimal

import pytest
from sqlalchemy import Engine

from app.common.enums.balance_enums import BalanceTypesEnum
from app.common.enums.transaction_enums import TransactionTypesEnum
from app.common.enums.user_enums import UserStatusesEnum
from app.common.enums.wallet_enums import WalletTypesEnum
from app.core.utils import get_hash
from app.database.base import Base
from app.di.container import build_container
from app.infrastructure.balances.schemas import CreateForeignBalanceSchema, CreateRegularBalanceSchema
from app.infrastructure.transactions.schemas import CreateDepositOrWithdrawTransactionSchema
from app.infrastructure.users.schemas import CloseUserSchema, CreateUserSchema
from app.infrastructure.users.use_cases import UserServiceFacade
from app.infrastructure.wallets.schemas import CreateWalletSchema
from app.infrastructure.wallets.use_cases import WalletServiceFacade


@pytest.fixture(autouse=True)
def start_test_db(container):
    engine = container.get(Engine)
    engine.dispose()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.fixture(scope='session', autouse=True)
def container():
    return build_container()


@pytest.fixture()
def load_client_to_db(container):
    facade = container.get(UserServiceFacade)

    schema = CreateUserSchema(key=UserStatusesEnum.CLIENT, name='loadClientTest', email='load_client_test@gmail.com', password='bw2fy728943tf&nh')
    return facade.create_user(schema)


@pytest.fixture()
def load_admin_to_db(container):
    facade = container.get(UserServiceFacade)

    schema = CreateUserSchema(key=UserStatusesEnum.ADMIN, name='loadAdminTest', email='load_admin_test@gmail.com', password='bw2fy728943tf&nh')
    return facade.create_user(schema)


@pytest.fixture()
def load_client_and_wallet_to_db(container):
    user_facade = container.get(UserServiceFacade)
    wallet_facade = container.get(WalletServiceFacade)

    user_schema = CreateUserSchema(key=UserStatusesEnum.CLIENT, name='loadClientTest', email='load_client_test@gmail.com', password='bw2fy728943tf&nh')
    user = user_facade.create_user(user_schema)

    wallet_schema = CreateWalletSchema(key=WalletTypesEnum.DEBIT, pin='1234')
    return wallet_facade.create_wallet(user, wallet_schema)


@pytest.fixture
def sample_create_client_schema():
    return CreateUserSchema(key=UserStatusesEnum.CLIENT, name='onetestsschema', email='testschema1@gmail.com', password='bw2fy728943tf&nh')


@pytest.fixture
def sample_create_admin_schema():
    return CreateUserSchema(key=UserStatusesEnum.ADMIN, name='twotestschema', email='testschema2@gmail.com', password='bw2fy728943tf&nh')


@pytest.fixture
def sample_close_user_schema():
    return CloseUserSchema(name='twotestschema', email='testschema2@gmail.com', password=get_hash('bw2fy728943tf&nh'))


@pytest.fixture
def sample_deposit_transaction():
    return CreateDepositOrWithdrawTransactionSchema(
        currency='USD',
        from_address='12345678909876543210987654',
        to_address='12345678909876543210987654',
        amount=Decimal(20),
        fee=Decimal(1.001),
        operation_type=TransactionTypesEnum.DEPOSIT,
    )


@pytest.fixture
def sample_regular_balance():
    return CreateRegularBalanceSchema(key=BalanceTypesEnum.REGULAR, amount=Decimal(20), currency='BYN')


@pytest.fixture
def sample_foreign_balance():
    return CreateForeignBalanceSchema(key=BalanceTypesEnum.FOREIGN, amounts=[Decimal(20), Decimal(3), Decimal(5)], currencies=['BYN', 'EUR', 'USD'])
