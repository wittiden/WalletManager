import pytest

from app.common.enums.user_enums import UserStatusesEnum
from app.infrastructure.users.factory import UserFactory


class TestUserFactory:
    """Класс для тестирования фабрики пользователей"""

    @pytest.mark.integration
    @pytest.mark.parametrize('key', [
        UserStatusesEnum.CLIENT,
        UserStatusesEnum.ADMIN,
    ])
    def test_create_user_good(self, container, sample_user_base, key):
        user_factory = container.get(UserFactory)

        user = user_factory.create_user(key, sample_user_base.name, sample_user_base.email, sample_user_base.password)
        assert user.status == key
        assert user.name == sample_user_base.name
        assert user.email == sample_user_base.email
        assert user.password == sample_user_base.password