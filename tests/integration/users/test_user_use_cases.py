import pytest

from app.common.enums.user_enums import UserStatusesEnum
from app.core.utils import get_hash
from app.infrastructure.users.schemas import CreateUserSchema, LoginUserSchema
from app.infrastructure.users.use_cases import UserServiceFacade


class TestUserServiceFacade:
    """Класс для тестирования работы фасада операций над пользователем"""

    @pytest.mark.integration
    @pytest.mark.parametrize('key, name, email, password', [
        (UserStatusesEnum.CLIENT, 'firsttest', 'test1@gmail.com', 'bw2fy728943tf&nh'),
        (UserStatusesEnum.ADMIN, 'twotest', 'test2@gmail.com', 'bw2fy728943tf&nh'),
    ])
    def test_create_user_good(self, container, key, name, email, password):
        schema = CreateUserSchema(key=key, name=name, email=email, password=password)

        facade = container.get(UserServiceFacade)

        user = facade.create_user(schema)
        assert user.name == name
        assert user.email == email
        assert user.password == get_hash(password)

    @pytest.mark.integration
    def test_login_user_good(self, container, sample_create_client_schema):
        facade = container.get(UserServiceFacade)

        facade.create_user(sample_create_client_schema)

        login_schema = LoginUserSchema(email=sample_create_client_schema.email, password=sample_create_client_schema.password)
        user = facade.login_user(login_schema)

        assert user.name == sample_create_client_schema.name
        assert user.email == sample_create_client_schema.email
        assert user.password == get_hash(sample_create_client_schema.password)

    @pytest.mark.integration
    def test_show_user_good(self, container, sample_create_admin_schema):
        facade = container.get(UserServiceFacade)

        user = facade.create_user(sample_create_admin_schema)

        find_user = facade.show_user(user, user.item_id)

        assert find_user.item_id == user.item_id
        assert find_user.name == user.name
        assert find_user.email == user.email
        assert find_user.password == user.password
        assert find_user.is_blocked == user.is_blocked
        assert find_user.status == user.status

    @pytest.mark.integration
    def test_block_user_good(self, container, sample_create_admin_schema):
        facade = container.get(UserServiceFacade)

        user = facade.create_user(sample_create_admin_schema)
        facade.block_user(user, user.item_id)

        blocked_user = facade.show_user(user, user.item_id)
        assert blocked_user.item_id == user.item_id
        assert blocked_user.name == user.name
        assert blocked_user.email == user.email
        assert blocked_user.password == user.password
        assert blocked_user.is_blocked is True
        assert blocked_user.status == user.status

    @pytest.mark.integration
    def test_unblock_user_good(self, container, sample_create_admin_schema):
        facade = container.get(UserServiceFacade)

        user = facade.create_user(sample_create_admin_schema)
        facade.block_user(user, user.item_id)

        facade.unblock_user(user, user.item_id)

        unblocked_user = facade.show_user(user, user.item_id)
        assert unblocked_user.item_id == user.item_id
        assert unblocked_user.name == user.name
        assert unblocked_user.email == user.email
        assert unblocked_user.password == user.password
        assert unblocked_user.is_blocked is False
        assert unblocked_user.status == user.status

    @pytest.mark.integration
    def test_close_user(self, container, sample_close_user_schema, sample_create_admin_schema):
        facade = container.get(UserServiceFacade)

        user = facade.create_user(sample_create_admin_schema)

        facade.close_user(sample_close_user_schema)

        with pytest.raises(ValueError):
            facade.show_my_user(user)