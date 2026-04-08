import pytest

from app.core.enums.user_enums import UserStatusesEnum
from app.core.utils.general_funcs import get_hash
from app.core.validations.exceptions import EmailValueExistsError, EmailValueNotExistsError, \
    PasswordValueNotExistsError, UserIsBlockedError, UserIsNotAdminError, AllParametersIsNoneError, IsNoneError, \
    UserIsNotBlockedError


@pytest.mark.unit
class TestCreateUserService:
    """Класс для тестирования сервиса по созданию пользователей"""

    @pytest.mark.parametrize('key, name, email, password', [
        (UserStatusesEnum.CLIENT, 'test', 'test@gmail.com', 'rjqlrhuqog&n324f'),
        (UserStatusesEnum.ADMIN, 'test', 'test2@gmail.com', 'rjqfwlrhu$qog324f')
    ])
    def test_create_user_good(self, create_user_service, key, name, email, password):
        user = create_user_service.create_user(key, name, email, password)
        assert user.name == name
        assert user.email == email
        assert user.password == get_hash(password)
        assert user.status == key

    @pytest.mark.parametrize('key, name, email, password, exception', [
        (UserStatusesEnum.CLIENT, 'test', 'test@gmail.com', 'rjqlrhuqog324f', EmailValueExistsError),
    ])
    def test_create_user_service_bad(self, create_user_service, key, name, email, password, exception):
        with pytest.raises(exception):
            create_user_service.create_user(UserStatusesEnum.CLIENT, 'test', 'test@gmail.com', 'rjqlrhuqog324f')
            create_user_service.create_user(key, name, email, password)


@pytest.mark.unit
class TestLoginUserService:
    """Класс для тестирования сервиса по входу в аккаунт пользователя"""

    def test_login_user_good(self, login_user_service, client_sample, create_user_service):
        create_user_service.create_user(client_sample.status, client_sample.name, client_sample.email, client_sample.password)
        user = login_user_service.login_user(client_sample.email, client_sample.password)
        assert user.email == client_sample.email
        assert user.password == get_hash(client_sample.password)

    @pytest.mark.parametrize('email, password, is_blocked, exceptions', [
        ('ipjuhp', 'h;uhhoh', False, EmailValueNotExistsError),
        ('test_client@gmail.com', 'bhwrlghg;wghlwrog', False, PasswordValueNotExistsError),
        ('test_client@gmail.com', 'bhwrlghgq951e;wghlwrog', True, UserIsBlockedError)
    ])
    def test_login_user_bad(self, login_user_service, client_sample, create_user_service, email, password, is_blocked, exceptions):
        user = create_user_service.create_user(client_sample.status, client_sample.name, client_sample.email, client_sample.password)
        user.is_blocked = is_blocked
        with pytest.raises(exceptions):
            login_user_service.login_user(email, password)


@pytest.mark.unit
class TestShowUserService:
    """Класс для тестирования сервиса по выводу информации пользователей"""

    def test_show_user_good(self, show_user_service, admin_sample, client_sample, create_user_service):
        first_user = create_user_service.create_user(client_sample.status, client_sample.name, client_sample.email, client_sample.password)
        user = show_user_service.show_user(admin_sample, first_user.item_id)
        assert user.name == client_sample.name
        assert user.email == client_sample.email

    def test_show_user_bad(self, show_user_service, admin_sample, client_sample, create_user_service):
        first_user = create_user_service.create_user(client_sample.status, client_sample.name, client_sample.email, client_sample.password)
        with pytest.raises(UserIsNotAdminError):
            show_user_service.show_user(client_sample, first_user.item_id)


@pytest.mark.unit
class TestSortUserService:
    """Класс для тестирования сервиса по сортировке пользователей"""

    def test_sort_user_good(self, sort_user_service, create_user_service, client_sample, admin_sample):
        create_user_service.create_user(client_sample.status, client_sample.name, client_sample.email, client_sample.password)
        sort_user_service.sort_users(admin_sample, item_id=True)

    @pytest.mark.parametrize('sample, exception', [
        ('admin', AllParametersIsNoneError),
        ('client',UserIsNotAdminError)
    ])
    def test_sort_user_bad(self, sort_user_service, create_user_service, client_sample, admin_sample, sample, exception):
        create_user_service.create_user(client_sample.status, client_sample.name, client_sample.email, client_sample.password)
        with pytest.raises(exception):
            if sample == 'admin':
                sort_user_service.sort_users(admin_sample)
            if sample == 'client':
                sort_user_service.sort_users(client_sample, is_blocked=True)


@pytest.mark.unit
class TestBlockUserService:
    """Класс для тестирования сервиса по блокировке и разблокировке пользователей"""

    def test_block_user_good(self, block_user_service, create_user_service, client_sample, admin_sample):
        first_user = create_user_service.create_user(client_sample.status, client_sample.name, client_sample.email, client_sample.password)

        block_user_service.block_user(admin_sample, first_user.item_id)
        assert first_user.is_blocked

    @pytest.mark.parametrize('sample, is_blocked, exception', [
        ('admin', True, UserIsBlockedError),
        ('client', False, UserIsNotAdminError),
        ('admin_is_none', False, IsNoneError)
    ])
    def test_block_user_bad(self, block_user_service, create_user_service, client_sample, admin_sample, is_blocked, sample, exception):
        first_user = create_user_service.create_user(client_sample.status, client_sample.name, client_sample.email, client_sample.password)
        first_user.is_blocked = is_blocked
        with pytest.raises(exception):
            if sample == 'admin':
                block_user_service.block_user(admin_sample, first_user.item_id)
            if sample == 'client':
                block_user_service.block_user(client_sample, first_user.item_id)
            if sample == 'admin_is_none':
                block_user_service.block_user(admin_sample, client_sample.item_id)

    def test_unblock_user_good(self, block_user_service, create_user_service, client_sample, admin_sample):
        first_user = create_user_service.create_user(client_sample.status, client_sample.name, client_sample.email, client_sample.password)
        first_user.is_blocked = True
        block_user_service.unblock_user(admin_sample, first_user.item_id)
        assert not first_user.is_blocked

    @pytest.mark.parametrize('sample, is_blocked, exception', [
        ('admin', False, UserIsNotBlockedError),
        ('client', True, UserIsNotAdminError),
        ('admin_is_none', True, IsNoneError)
    ])
    def test_unblock_user_bad(self, block_user_service, create_user_service, client_sample, admin_sample, is_blocked, sample, exception):
        first_user = create_user_service.create_user(client_sample.status, client_sample.name, client_sample.email, client_sample.password)
        first_user.is_blocked = is_blocked
        with pytest.raises(exception):
            if sample == 'admin':
                block_user_service.unblock_user(admin_sample, first_user.item_id)
            if sample == 'client':
                block_user_service.unblock_user(client_sample, first_user.item_id)
            if sample == 'admin_is_none':
                block_user_service.unblock_user(admin_sample, client_sample.item_id)