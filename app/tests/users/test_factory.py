import pytest

from app.core.enums.user_enums import UserStatusesEnum
from app.tests.users.conftest import user_registrations
from app.users.domain import Client, Admin


@pytest.mark.unit
class TestUserFactory:
    """Класс для тестирования фабрики по созданию пользователя"""

    @pytest.mark.parametrize('key, name, email, password', [
        (UserStatusesEnum.CLIENT, 'denis', 'ar.den@gmail.com', 'wrlvjw&r3243a84el'),
        (UserStatusesEnum.ADMIN, 'tomal', 'test@mail.ru', 'rehqglhrgferf88*oqeh')
    ])
    def test_create_user(self, key, name, email, password, user_factory):
        user = user_factory.create_user(key, name, email, password)
        assert user.status == key
        assert user.name == name
        assert user.email == email
        assert user.password == password


@pytest.mark.unit
class TestUserRegistrations:
    """"""

    @pytest.mark.parametrize('key, value', [
        (UserStatusesEnum.CLIENT, Client),
        (UserStatusesEnum.ADMIN, Admin)
    ])
    def test_user_registrations_good(self, key, value, user_registrations):
        user_registrations.set_registration(key, value)

        assert user_registrations.get_registration(key) == value
