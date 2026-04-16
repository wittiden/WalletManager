import pytest
from app.infrastructure.users.domain import Client, Admin


@pytest.fixture
def client_sample() -> 'Client':
    return Client('test_client', 'test_client@gmail.com', 'bhwrlghgq951e;wghlwrog')


@pytest.fixture
def admin_sample() -> 'Admin':
    return Admin('test_admin', 'test_admin@gmail.com', 'wbgrlghwglhqowihgeuvw')