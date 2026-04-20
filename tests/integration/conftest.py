import pytest

from app.di.container import build_container


@pytest.fixture(scope="session", autouse=True)
def container():
    return build_container()