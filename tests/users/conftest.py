import pytest
from app.users.factory import UserFactory, UserRegistrations
from app.common.enums.user_enums import UserStatusesEnum
from app.users.domain import Admin, Client
from app.users.repository.repository import UserRepository
from app.users.use_cases import UserServiceFacade, CreateUserService, LoginUserService, SortUserService, ShowUserService, BlockUserService


@pytest.fixture(scope='package')
def user_registrations() -> 'UserRegistrations':
    user_registration = UserRegistrations()
    user_registration.set_registration(UserStatusesEnum.CLIENT, Client)
    user_registration.set_registration(UserStatusesEnum.ADMIN, Admin)
    return user_registration

@pytest.fixture(scope='package')
def user_factory(user_registrations: 'UserRegistrations') -> 'UserFactory':
    return UserFactory(user_registrations)

@pytest.fixture
def user_repository() -> 'UserRepository':
    return UserRepository()

@pytest.fixture
def create_user_service(user_repository: 'UserRepository', user_factory: 'UserFactory') -> 'CreateUserService':
    return CreateUserService(user_repository, user_factory)

@pytest.fixture
def login_user_service(user_repository: 'UserRepository') -> 'LoginUserService':
    return LoginUserService(user_repository)

@pytest.fixture
def sort_user_service(user_repository: 'UserRepository') -> 'SortUserService':
    return SortUserService(user_repository)

@pytest.fixture
def show_user_service(user_repository: 'UserRepository') -> 'ShowUserService':
    return ShowUserService(user_repository)

@pytest.fixture
def block_user_service(user_repository: 'UserRepository') -> 'BlockUserService':
    return BlockUserService(user_repository)

@pytest.fixture
def user_service_facade(create_user_service: 'CreateUserService', login_user_service: 'LoginUserService', sort_user_service: 'SortUserService', show_user_service: 'ShowUserService', block_user_service: 'BlockUserService') -> 'UserServiceFacade':
    return UserServiceFacade(create_user_service, login_user_service, show_user_service, block_user_service, sort_user_service)