from dishka import Provider, provide, make_container, Scope
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database.config import Settings
from app.common.enums.balance_enums import BalanceTypesEnum
from app.common.enums.transaction_enums import TransactionTypesEnum
from app.common.enums.user_enums import UserStatusesEnum
from app.common.enums.wallet_enums import WalletTypesEnum
from app.infrastructure.balances.domain import RegularBalance, ForeignBalance
from app.infrastructure.balances.factory import BalanceFactory, BalanceRegistry
from app.infrastructure.balances.repository.commands import BalanceCommandsRepository
from app.infrastructure.balances.repository.mapper import BalanceMapper
from app.infrastructure.balances.use_cases import CreateBalanceService, ShowBalanceService, FreezeBalanceService, \
    BalanceServiceFacade
from app.infrastructure.transactions.domain import DepositTransaction, WithdrawTransaction, ExchangeTransaction
from app.infrastructure.transactions.factory import TransactionFactory, TransactionRegistry
from app.infrastructure.transactions.repository.commands import TransactionCommandsRepository
from app.infrastructure.transactions.repository.mapper import TransactionMapper
from app.infrastructure.transactions.repository.queries import TransactionQueriesRepository
from app.infrastructure.transactions.use_cases import CreateTransactionService, ShowTransactionService, \
    SortTransactionService, TransactionServiceFacade
from app.infrastructure.users.domain import Client, Admin
from app.infrastructure.users.factory import UserFactory, UserRegistrations
from app.infrastructure.users.repository.commands import UserCommandsRepository
from app.infrastructure.users.repository.mapper import UserMapper
from app.infrastructure.users.repository.queries import UserQueriesRepository
from app.infrastructure.users.use_cases import CreateUserService, LoginUserService, ShowUserService, SortUserService, \
    BlockUserService, CloseUserService, UserServiceFacade
from app.infrastructure.wallets.domain import DebitWallet, CreditWallet
from app.infrastructure.wallets.factory import WalletFactory, WalletFactoryRegistry
from app.infrastructure.wallets.repository.commands import WalletCommandsRepository
from app.infrastructure.wallets.repository.mapper import WalletMapper
from app.infrastructure.wallets.repository.queries import WalletQueriesRepository
from app.infrastructure.wallets.use_cases import CreateWalletService, ShowWalletService, SortWalletService, \
    BlockWalletService, CloseWalletService, WalletServiceFacade


class FactoryProvider(Provider):
    """Класс провайдер по созданию фабрик"""

    scope = Scope.APP

    @provide
    def user_factory(self) -> 'UserFactory':
        user_registrations = UserRegistrations()
        user_registrations.set_registration(UserStatusesEnum.CLIENT, Client)
        user_registrations.set_registration(UserStatusesEnum.ADMIN, Admin)
        return UserFactory(user_registrations)

    @provide
    def wallet_factory(self) -> 'WalletFactory':
        wallet_registration = WalletFactoryRegistry()
        wallet_registration.set_registration(WalletTypesEnum.DEBIT, DebitWallet)
        wallet_registration.set_registration(WalletTypesEnum.CREDIT, CreditWallet)
        return WalletFactory(wallet_registration)

    @provide
    def balance_factory(self) -> 'BalanceFactory':
        balance_registration = BalanceRegistry()
        balance_registration.set_registration(BalanceTypesEnum.REGULAR, RegularBalance)
        balance_registration.set_registration(BalanceTypesEnum.FOREIGN, ForeignBalance)
        return BalanceFactory(balance_registration)

    @provide
    def transaction_factory(self) -> 'TransactionFactory':
        transaction_registration = TransactionRegistry()
        transaction_registration.set_registration(TransactionTypesEnum.DEPOSIT, DepositTransaction)
        transaction_registration.set_registration(TransactionTypesEnum.WITHDRAW, WithdrawTransaction)
        transaction_registration.set_registration(TransactionTypesEnum.EXCHANGE, ExchangeTransaction)
        return TransactionFactory(transaction_registration)


class MapperProvider(Provider):
    """Класс провайдер по созданию мапперов"""

    scope = Scope.APP

    @provide
    def user_mapper(self, user_factory: 'UserFactory') -> 'UserMapper':
        return UserMapper(user_factory)

    @provide
    def wallet_mapper(self, wallet_factory: 'WalletFactory') -> 'WalletMapper':
        return WalletMapper(wallet_factory)

    @provide
    def balance_mapper(self, balance_factory: 'BalanceFactory') -> 'BalanceMapper':
        return BalanceMapper(balance_factory)

    @provide
    def transaction_mapper(self, transaction_factory: 'TransactionFactory') -> 'TransactionMapper':
        return TransactionMapper(transaction_factory)


class DatabaseSettingsProvider(Provider):
    """Класс провайдер по созданию настроек бд"""

    scope = Scope.APP

    @provide
    def database_settings(self) -> 'Settings':
        return Settings()


class DatabaseEngineProvider(Provider):
    """Класс провайдер по созданию движка бд"""

    scope = Scope.APP

    @provide
    def database_create_engine(self, settings: 'Settings') -> Engine:
        return create_engine(
            settings.database_url_psycopg,
            echo=False,
            pool_size=5,
            max_overflow=10
        )

    @provide
    def database_create_async_engine(self, settings: 'Settings') -> AsyncEngine:
        return create_async_engine(
            settings.database_url_asyncpg,
            echo=False
        )


class DatabaseSessionProvider(Provider):
    """Класс провайдер по созданию фабрики сессий бд"""

    scope = Scope.APP

    @provide
    def database_create_session_factory(self, engine: Engine) -> sessionmaker:
        return sessionmaker(engine)

    @provide
    def database_create_async_session_factory(self, async_engine: 'AsyncEngine') -> async_sessionmaker:
        return async_sessionmaker(async_engine)


class RepositoryProvider(Provider):
    """Класс провайдер по созданию команд и запросов"""

    scope = Scope.APP

    @provide
    def user_commands_repo(self, session_factory: sessionmaker, user_mapper: 'UserMapper') -> 'UserCommandsRepository':
        return UserCommandsRepository(session_factory, user_mapper)

    @provide
    def user_queries_repo(self, session_factory: sessionmaker, user_mapper: 'UserMapper', wallet_mapper: 'WalletMapper') -> 'UserQueriesRepository':
        return UserQueriesRepository(session_factory, user_mapper, wallet_mapper)

    @provide
    def wallet_commands_repo(self, session_factory: sessionmaker, wallet_mapper: 'WalletMapper') -> 'WalletCommandsRepository':
        return WalletCommandsRepository(session_factory, wallet_mapper)

    @provide
    def wallet_queries_repo(self, session_factory: sessionmaker, wallet_mapper: 'WalletMapper', balance_mapper: 'BalanceMapper') -> 'WalletQueriesRepository':
        return WalletQueriesRepository(session_factory, wallet_mapper, balance_mapper)

    @provide
    def balance_commands_repo(self, session_factory: sessionmaker, balance_mapper: 'BalanceMapper') -> 'BalanceCommandsRepository':
        return BalanceCommandsRepository(session_factory, balance_mapper)

    @provide
    def transaction_commands_repo(self, session_factory: sessionmaker, transaction_mapper: 'TransactionMapper') -> 'TransactionCommandsRepository':
        return TransactionCommandsRepository(session_factory, transaction_mapper)

    @provide
    def transaction_queries_repo(self, session_factory: sessionmaker, transaction_mapper: 'TransactionMapper') -> 'TransactionQueriesRepository':
        return TransactionQueriesRepository(session_factory, transaction_mapper)


class FacadeProvider(Provider):
    """Класс провайдер по созданию фасадов"""

    scope = Scope.APP

    @provide
    def user_service_facade(self, user_factory: 'UserFactory', user_commands_repository: 'UserCommandsRepository', user_queries_repository: 'UserQueriesRepository') -> 'UserServiceFacade':
        create_user_service = CreateUserService(user_factory, user_commands_repository)
        login_user_service = LoginUserService(user_queries_repository)
        show_user_service = ShowUserService(user_queries_repository)
        sort_user_service = SortUserService(user_queries_repository)
        block_user_service = BlockUserService(user_queries_repository, user_commands_repository)
        close_user_service = CloseUserService(user_commands_repository, user_queries_repository)
        return UserServiceFacade(create_user_service, login_user_service, show_user_service, block_user_service, sort_user_service, close_user_service)

    @provide
    def wallet_service_facade(self, wallet_factory: 'WalletFactory', wallet_commands_repository: 'WalletCommandsRepository', wallet_queries_repository: 'WalletQueriesRepository', user_commands_repository: 'UserCommandsRepository') -> 'WalletServiceFacade':
        create_wallet_service = CreateWalletService(wallet_factory, wallet_commands_repository, user_commands_repository)
        show_wallet_service = ShowWalletService(wallet_queries_repository)
        sort_wallet_service = SortWalletService(wallet_queries_repository)
        block_wallet_service = BlockWalletService(wallet_commands_repository, wallet_queries_repository)
        close_wallet_service = CloseWalletService(wallet_commands_repository, wallet_queries_repository)
        return WalletServiceFacade(create_wallet_service, show_wallet_service, sort_wallet_service, block_wallet_service, close_wallet_service)

    @provide
    def balance_service_facade(self, balance_factory: 'BalanceFactory', balance_commands_repository: 'BalanceCommandsRepository', wallet_queries_repository: 'WalletQueriesRepository') -> 'BalanceServiceFacade':
        create_balance_service = CreateBalanceService(balance_factory, balance_commands_repository)
        show_balance_service = ShowBalanceService(wallet_queries_repository)
        freeze_balance_service = FreezeBalanceService(wallet_queries_repository, balance_commands_repository)
        return BalanceServiceFacade(create_balance_service, show_balance_service, freeze_balance_service)

    @provide
    def transaction_service_facade(self, transaction_factory: 'TransactionFactory', transaction_commands_repository: 'TransactionCommandsRepository', transaction_queries_repository: 'TransactionQueriesRepository') -> 'TransactionServiceFacade':
        create_transaction_service = CreateTransactionService(transaction_factory, transaction_commands_repository)
        show_transaction_service = ShowTransactionService(transaction_queries_repository)
        sort_transaction_service = SortTransactionService(transaction_queries_repository)
        return TransactionServiceFacade(create_transaction_service, show_transaction_service, sort_transaction_service)


def build_container():
    return make_container(FactoryProvider(), MapperProvider(), DatabaseSettingsProvider(), DatabaseEngineProvider(), DatabaseSessionProvider(), RepositoryProvider(), FacadeProvider())
