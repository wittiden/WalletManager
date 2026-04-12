from typing import TYPE_CHECKING

from app.common.enums.user_enums import UserStatusesEnum
from app.core.decorators import debug_log, info_log
from app.core.exceptions import EmailValueExistsError, PasswordValueNotExistsError, UserIsBlockedError, \
    EmailValueNotExistsError, AllParametersIsNoneError, UserIsNotBlockedError
from app.core.utils import get_hash
from app.core.validations import GeneralValidation, UseCasesValidation
from app.users.schemas import CreateUserSchema, LoginUserSchema

if TYPE_CHECKING:
    from app.users.domain import UserBase
    from app.users.factory import UserFactory
    from app.users.repository.repository import UserRepository


class UserServiceFacade:
    """Фасадный сервис класс для управления сервисами"""

    def __init__(self, create_user_service: 'CreateUserService', login_user_service: 'LoginUserService', show_user_service: 'ShowUserService', block_user_service: 'BlockUserService', sort_user_service: 'SortUserService') -> None:
        self._create_user_service = create_user_service
        self._login_user_service = login_user_service
        self._show_user_service = show_user_service
        self._block_user_service = block_user_service
        self._sort_user_service = sort_user_service

    @debug_log
    @info_log(['', 'Пользователь создан'])
    def create_user(self, schema: 'CreateUserSchema') -> 'UserBase':
        return self._create_user_service.create_user(schema.key, schema.name, schema.email, schema.password)

    @debug_log
    @info_log(['', 'Вы вошли в аккаунт'])
    def login_user(self, schema: 'LoginUserSchema') -> 'UserBase':
        return self._login_user_service.login_user(schema.email, schema.password)

    @debug_log
    @info_log(['', 'Пользователь создан и вход выполнен'])
    def create_and_login_user(self, schema: 'CreateUserSchema') -> 'UserBase':
        self.create_user(schema)
        return self.login_user(schema)

    @debug_log
    @info_log(['Информация о пользователе:', ''])
    def show_user(self, user: 'UserBase', find_user_id: str) -> 'UserBase':
        return self._show_user_service.show_user(user, find_user_id)

    @debug_log
    @info_log(['Информация о пользователях:', ''])
    def show_all_users(self, user: 'UserBase') -> list['UserBase']:
        return self._show_user_service.show_all_users(user)

    @debug_log
    @info_log(['Информация о моем пользователе:', ''])
    def show_my_user(self, user: 'UserBase') -> 'UserBase':
        return self._show_user_service.show_my_user(user)

    @debug_log
    @info_log(['Сортировка пользователей:', ''])
    def sort_users(self, user: 'UserBase', item_id: bool = None, name: bool = None, email: bool = None, password: bool = None, is_blocked: bool = None) -> list:
        return self._sort_user_service.sort_users(user, item_id, name, email, password, is_blocked)

    @debug_log
    @info_log(['', 'Пользователь заблокирован'])
    def block_user(self, user: 'UserBase', find_user_id: str) -> None:
        self._block_user_service.block_user(user, find_user_id)

    @debug_log
    @info_log(['', 'Пользователь разблокирован'])
    def unblock_user(self, user: 'UserBase', find_user_id: str) -> None:
        self._block_user_service.unblock_user(user, find_user_id)


class CreateUserService:
    """Сервис класс по созданию пользователя"""

    def __init__(self, repository: 'UserRepository', user_factory: 'UserFactory') -> None:
        self._repository = repository
        self._user_factory = user_factory

    def create_user(self, key: 'UserStatusesEnum', name: str, email: str, password: str) -> 'UserBase':
        for user in self._repository.get_all_users():
            if user.email == email:
                raise EmailValueExistsError

        user = self._user_factory.create_user(key, name, email, get_hash(password))
        GeneralValidation.not_none_checker(user)

        self._repository.add_user(user)
        return user


class LoginUserService:
    """Сервис класс для входа в аккаунт"""

    def __init__(self, repository: 'UserRepository') -> None:
        self._repository = repository

    def login_user(self, email: str, password: str) -> 'UserBase':
        for user in self._repository.get_all_users():
            if user.email == email:
                if user.password != get_hash(password):
                    raise PasswordValueNotExistsError
                if user.is_blocked:
                    raise UserIsBlockedError
                return user

        raise EmailValueNotExistsError


class ShowUserService:
    """Сервис класс для вывода информации о пользователе"""

    def __init__(self, repository: 'UserRepository') -> None:
        self._repository = repository

    def show_user(self, user: 'UserBase', find_user_id: str) -> 'UserBase':
        UseCasesValidation.is_admin_checker(user)

        return GeneralValidation.not_none_checker(self._repository.get_user(find_user_id))

    def show_all_users(self, user: 'UserBase') -> list[UserBase]:
        UseCasesValidation.is_admin_checker(user)

        return GeneralValidation.not_none_checker(self._repository.get_all_users())

    def show_my_user(self, user: 'UserBase') -> 'UserBase':
        return GeneralValidation.not_none_checker(self._repository.get_user(user.item_id))


class SortUserService:
    """Сервис класс для сортировки данных пользователя"""

    def __init__(self, repository: 'UserRepository') -> None:
        self._repository = repository

    def sort_users(self, user: 'UserBase', item_id: bool = None, name: bool = None, email: bool = None, password: bool = None, is_blocked: bool = None) -> list['UserBase']:
        UseCasesValidation.is_admin_checker(user)

        all_users = GeneralValidation.not_none_checker(self._repository.get_all_users())

        attrib_dict: dict[str, bool] = {'item_id': item_id, 'name': name, 'email': email, 'password': password, 'is_blocked': is_blocked}
        for key, value in attrib_dict.items():
            if value:
                sorted_result: list['UserBase'] = sorted(all_users, key=lambda r : getattr(r, key))
                return sorted_result

        raise AllParametersIsNoneError


class BlockUserService:
    """Сервис класс для блокировки и разблокировки пользователя"""

    def __init__(self, repository: 'UserRepository') -> None:
        self._repository = repository

    def block_user(self, user: 'UserBase', find_user_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        find_user = GeneralValidation.not_none_checker(self._repository.get_user(find_user_id))
        if find_user.is_blocked:
            raise UserIsBlockedError
        find_user.is_blocked = True

    def unblock_user(self, user: 'UserBase', find_user_id: str) -> None:
        UseCasesValidation.is_admin_checker(user)

        find_user = GeneralValidation.not_none_checker(self._repository.get_user(find_user_id))
        if not find_user.is_blocked:
            raise UserIsNotBlockedError
        find_user.is_blocked = False