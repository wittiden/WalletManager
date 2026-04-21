from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from app.common.enums.user_enums import UserStatusesEnum
from app.core.decorators import debug_log, info_log
from app.core.exceptions import UserIsBlockedError, UserIsNotBlockedError
from app.core.utils import get_hash
from app.core.validations import GeneralValidation, UseCasesValidation
from app.infrastructure.users.schemas import CloseUserSchema

if TYPE_CHECKING:
    from app.infrastructure.users.domain import UserBase
    from app.infrastructure.users.factory import UserFactory
    from app.infrastructure.users.repository.commands import UserCommandsRepository
    from app.infrastructure.users.repository.queries import UserQueriesRepository
    from app.infrastructure.users.schemas import CreateUserSchema, LoginUserSchema


class UserServiceFacade:
    """Фасадный сервис класс для управления сервисами"""

    def __init__(
        self,
        create_user_service: 'CreateUserService',
        login_user_service: 'LoginUserService',
        show_user_service: 'ShowUserService',
        block_user_service: 'BlockUserService',
        sort_user_service: 'SortUserService',
        close_user_service: 'CloseUserService',
    ) -> None:
        self._create_user_service = create_user_service
        self._login_user_service = login_user_service
        self._show_user_service = show_user_service
        self._block_user_service = block_user_service
        self._sort_user_service = sort_user_service
        self._close_user_service = close_user_service

    @debug_log
    @info_log(strat_info=None, end_info='Пользователь создан')
    def create_user(self, schema: 'CreateUserSchema') -> 'UserBase':
        return self._create_user_service.create_user(schema.key, schema.name, schema.email, schema.password)

    @debug_log
    @info_log(strat_info=None, end_info='Вы вошли в аккаунт')
    def login_user(self, schema: 'LoginUserSchema') -> 'UserBase':
        return self._login_user_service.login_user(schema.email, schema.password)

    @debug_log
    @info_log(strat_info='Информация о пользователе:', end_info=None)
    def show_user(self, user: 'UserBase', find_user_id: str) -> 'UserBase':
        return self._show_user_service.show_user(user, find_user_id)

    @debug_log
    @info_log(strat_info='Информация о пользователях:', end_info=None)
    def show_all_users(self, user: 'UserBase') -> list['UserBase']:
        return self._show_user_service.show_all_users(user)

    @debug_log
    @info_log(strat_info='Информация о вашем пользователе:', end_info=None)
    def show_my_user(self, user: 'UserBase') -> 'UserBase':
        return self._show_user_service.show_my_user(user)

    @debug_log
    @info_log(strat_info='Отсортированная информация о пользователях:', end_info=None)
    def sort_users(self, user: 'UserBase', order_by_param: str) -> list:
        return self._sort_user_service.sort_users(user, order_by_param)

    @debug_log
    @info_log(strat_info=None, end_info='Пользователь заблокирован')
    def block_user(self, user: 'UserBase', find_user_id: str) -> None:
        self._block_user_service.block_user(user, find_user_id)

    @debug_log
    @info_log(strat_info=None, end_info='Пользователь разблокирован')
    def unblock_user(self, user: 'UserBase', find_user_id: str) -> None:
        self._block_user_service.unblock_user(user, find_user_id)

    @debug_log
    @info_log(strat_info=None, end_info='Аккаунт закрыт')
    def close_user(self, schema: 'CloseUserSchema') -> None:
        self._close_user_service.close_user(schema.name, schema.email, schema.password)


class CreateUserService:
    """Сервис класс по созданию пользователя"""

    def __init__(self, user_factory: 'UserFactory', user_commands_repository: 'UserCommandsRepository') -> None:
        self._user_factory = user_factory
        self._user_commands_repository = user_commands_repository

    def create_user(self, key: 'UserStatusesEnum', name: str, email: str, password: str) -> 'UserBase':
        user = self._user_factory.create_user(key, name, email, get_hash(password))
        GeneralValidation.not_none_checker(user)

        try:
            self._user_commands_repository.insert_user_info(user)
        except IntegrityError:
            raise

        return user


class LoginUserService:
    """Сервис класс для входа в аккаунт"""

    def __init__(self, user_queries_repository: 'UserQueriesRepository') -> None:
        self._user_queries_repository = user_queries_repository

    def login_user(self, email: str, password: str) -> 'UserBase':
        user = self._user_queries_repository.select_user_for_email_and_pass(email, get_hash(password))
        GeneralValidation.not_none_checker(user)

        if user.is_blocked:
            raise UserIsBlockedError

        return user


class ShowUserService:
    """Сервис класс для вывода информации о пользователе"""

    def __init__(self, user_queries_repository: 'UserQueriesRepository') -> None:
        self._user_queries_repository = user_queries_repository

    def show_user(self, user: 'UserBase', find_user_id: str) -> 'UserBase':
        UseCasesValidation.is_admin_checker(user)

        return GeneralValidation.not_none_checker(self._user_queries_repository.select_user(find_user_id))

    def show_all_users(self, user: 'UserBase') -> list[UserBase]:
        UseCasesValidation.is_admin_checker(user)

        return self._user_queries_repository.select_all_users()

    def show_my_user(self, user: 'UserBase') -> 'UserBase':
        return GeneralValidation.not_none_checker(self._user_queries_repository.select_my_user(user))


class SortUserService:
    """Сервис класс для сортировки данных пользователя"""

    def __init__(self, user_queries_repository: 'UserQueriesRepository') -> None:
        self._user_queries_repository = user_queries_repository

    def sort_users(self, user: 'UserBase', order_by_param: str) -> list['UserBase']:
        UseCasesValidation.is_admin_checker(user)

        return self._user_queries_repository.select_order_by_users(order_by_param)


class BlockUserService:
    """Сервис класс для блокировки и разблокировки пользователя"""

    def __init__(self, user_queries_repository: 'UserQueriesRepository', user_commands_repository: 'UserCommandsRepository') -> None:
        self._user_queries_repository = user_queries_repository
        self._user_commands_repository = user_commands_repository

    def block_user(self, user: 'UserBase', find_user_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        find_user = GeneralValidation.not_none_checker(self._user_queries_repository.select_user(find_user_id))
        if find_user.is_blocked:
            raise UserIsBlockedError

        self._user_commands_repository.update_user_info(find_user, {'is_blocked': True})

    def unblock_user(self, user: 'UserBase', find_user_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        find_user = GeneralValidation.not_none_checker(self._user_queries_repository.select_user(find_user_id))
        if not find_user.is_blocked:
            raise UserIsNotBlockedError

        self._user_commands_repository.update_user_info(find_user, {'is_blocked': False})


class CloseUserService:
    """Сервис класс для закрытия аккаунта пользователя"""

    def __init__(self, user_commands_repository: 'UserCommandsRepository', user_queries_repository: 'UserQueriesRepository') -> None:
        self._user_commands_repository = user_commands_repository
        self._user_queries_repository = user_queries_repository

    def close_user(self, name: str, email: str, password: str) -> None:
        user = self._user_queries_repository.select_user_for_email_and_pass(email, password)
        GeneralValidation.not_none_checker(user)
        if user.name != name:
            raise ValueError

        self._user_commands_repository.delete_user_info(user)
