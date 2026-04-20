import pytest
from sqlalchemy import Engine

from app.common.enums.user_enums import UserStatusesEnum
from app.core.utils import get_hash
from app.database.base import Base
from app.di.container import build_container
from app.infrastructure.users.schemas import CreateUserSchema, CloseUserSchema
from app.infrastructure.users.use_cases import UserServiceFacade


@pytest.fixture(autouse=True)
def start_test_db(container):
    engine = container.get(Engine)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

@pytest.fixture(scope="session", autouse=True)
def container():
    return build_container()

@pytest.fixture()
def load_client_to_db(container):
    facade = container.get(UserServiceFacade)

    schema = CreateUserSchema(key=UserStatusesEnum.CLIENT ,name='loadClientTest', email='load_client_test@gmail.com', password='bw2fy728943tf&nh')
    return facade.create_user(schema)

@pytest.fixture()
def load_admin_to_db(container):
    facade = container.get(UserServiceFacade)

    schema = CreateUserSchema(key=UserStatusesEnum.ADMIN ,name='loadAdminTest', email='load_admin_test@gmail.com', password='bw2fy728943tf&nh')
    return facade.create_user(schema)

@pytest.fixture
def sample_create_client_schema():
    return CreateUserSchema(key=UserStatusesEnum.CLIENT, name='onetestsschema', email='testschema1@gmail.com', password='bw2fy728943tf&nh')

@pytest.fixture
def sample_create_admin_schema():
    return CreateUserSchema(key=UserStatusesEnum.ADMIN, name='twotestschema', email='testschema2@gmail.com', password='bw2fy728943tf&nh')

@pytest.fixture
def sample_close_user_schema():
    return CloseUserSchema(name='twotestschema', email='testschema2@gmail.com', password=get_hash('bw2fy728943tf&nh'))