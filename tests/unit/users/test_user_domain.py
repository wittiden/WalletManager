import pytest
from pytest_mock import MockerFixture

from app.common.enums.user_enums import UserStatusesEnum
from app.infrastructure.users.domain import UserBase, Client, Admin


class TestUserDomain:
    """Класс для тестирования домена пользователя"""

    @pytest.mark.unit
    @pytest.mark.parametrize('class_type, name, email, password, status', [
        (UserBase, 'test', 'test@gmail.com', 'pass12345', UserStatusesEnum.UNKNOWN),
        (Client, 'test', 'test@gmail.com', 'pass12345', UserStatusesEnum.CLIENT),
        (Admin, 'test', 'test@gmail.com', 'pass12345', UserStatusesEnum.ADMIN),
    ])
    def test_user_base_good(self, class_type, name, email, password, status):
        obj = class_type(name, email, password)
        assert obj.name == name
        assert obj.email == email
        assert obj.password == password
        assert obj.status == status

    @pytest.mark.unit
    @pytest.mark.parametrize('name, email, password, is_blocked', [
        ('', 'test@gmail.com', 'pass12345', False),
        ('test', '', 'pass12345', False),
        ('test', 'test@gmail.com', '', False),
        ('test', 'test@gmail.com', 'pass12345', ''),
    ])
    def test_user_base_bad(self, name, email, password, is_blocked):
        with pytest.raises(ValueError):
            UserBase(name, email, password, is_blocked)

    @pytest.mark.unit
    def test_user_setters(self, sample_user_base, mocker: MockerFixture):
        mock = mocker.patch('app.infrastructure.users.domain.user_upgrade_signal.send')

        sample_user_base.name = 'name'
        sample_user_base.email = 'email@gmail.com'

        assert mock.call_count == 2

