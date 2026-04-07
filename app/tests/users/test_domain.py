import pytest

from app.core.utils.general_funcs import get_hash
from app.core.validations.exceptions import EmailFormatError, PasswordFormatError, \
    NameFormatError, IsEmptyError
from app.users.domain import Client, Admin


@pytest.mark.unit
class TestUserBase:
    """Класс для тестирования создания пользователя разных типов напрямую"""

    @pytest.mark.parametrize('key, name, email, password', [
        ('client_sample', 'test_client', 'test_client@gmail.com', 'bhwrlghgq951e;wghlwrog'),
        ('admin_sample', 'test_admin', 'test_admin@gmail.com', 'wbgrlghwglhqowihgeuvw'),
        ('client', 'param_test', 'param_test@gmail.com', 'bqfkgqywgfigfi'),
        ('admin', 'param_test2', 'param_test2@gmail.com', ';qfnbqfkgqywgfigfi')
    ])
    def test_user_good(self, key, name, email, password, client_sample, admin_sample):
        if key == 'client_sample':
            assert client_sample.name == name
            assert client_sample.email == email
            assert client_sample.password == get_hash(password)

        elif key == 'admin_sample':
            assert admin_sample.name == name
            assert admin_sample.email == email
            assert admin_sample.password == get_hash(password)

        elif key == 'client':
            user = Admin(name, email, password)
            assert user.name == name
            assert user.email == email
            assert user.password == get_hash(password)

    @pytest.mark.parametrize('key, name, email, password, exception', [
        ('client', '432j', 'param_test@gmail.com', 'bqfkgqywgfigfi', NameFormatError),
        ('client', 'gre4ege32', 'param_test@gmail.com', 'bqfkgqywgfigfi', NameFormatError),
        ('client', 'test', 'param_test@@gmail.com', 'bqfkgqywgfigfi', EmailFormatError),
        ('client', 'test', '@gmail.com', 'bqfkgqywgfigfi', IsEmptyError),
        ('client', 'test', 'param_test@', 'bqfkgqywgfigfi', IsEmptyError),
        ('admin', 'test', 'param_test2@gmail.com', ';', PasswordFormatError)
    ])
    def test_user_bad(self, key, name, email, password, exception):
        with pytest.raises(exception):
            if key == 'client':
                assert Client(name, email, password)

            if key == 'admin':
                assert Admin(name, email, password)
