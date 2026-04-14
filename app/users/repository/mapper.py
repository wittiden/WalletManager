from app.database.models.user import UserTable
from app.users.domain import UserBase, Client, Admin
from app.common.enums.user_enums import UserStatusesEnum


class UserMapper:
    """Mapper класс для преобразования user->orm_user, orm_user->user"""

    @staticmethod
    def domain_to_table(user: 'UserBase') -> 'UserTable':
        obj = UserTable(name=user.name, email=user.email, password=user.password, is_blocked=user.is_blocked, status=user.status)
        obj.user_id = user.item_id
        return obj

    @staticmethod
    def table_to_domain(user_table: 'UserTable') -> 'UserBase':
        if user_table.status == UserStatusesEnum.CLIENT:
            obj = Client(_name=user_table.name, _email=user_table.email, _password=user_table.password, _is_blocked=user_table.is_blocked, _wallets=user_table.wallets)

        elif user_table.status == UserStatusesEnum.ADMIN:
            obj = Admin(_name=user_table.name, _email=user_table.email, _password=user_table.password, _is_blocked=user_table.is_blocked)

        else:
            raise ValueError(f"Unknown status: {user_table.status}")

        obj.item_id = user_table.user_id
        return obj