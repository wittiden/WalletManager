from app.common.enums.balance_enums import BalanceTypesEnum
from app.common.enums.transaction_enums import TransactionTypesEnum
from app.common.enums.user_enums import UserStatusesEnum
from app.common.enums.wallet_enums import WalletTypesEnum
from app.core.logger import add_logger
from app.infrastructure.balances.domain import RegularBalance, ForeignBalance
from app.infrastructure.balances.factory import BalanceFactory, BalanceRegistry
from app.infrastructure.balances.repository.commands import BalanceCommandsRepository
from app.infrastructure.balances.repository.mapper import BalanceMapper
from app.infrastructure.balances.repository.queries import BalanceQueriesRepository
from app.infrastructure.transactions.repository.mapper import TransactionMapper
from app.infrastructure.users.domain import Client, Admin
from app.infrastructure.users.factory import UserRegistrations, UserFactory
from app.infrastructure.users.repository.commands import UserCommandsRepository
from app.database.engine import session_factory
from app.infrastructure.users.repository.mapper import UserMapper
from app.infrastructure.users.repository.queries import UserQueriesRepository
from app.infrastructure.users.use_cases import CreateUserService, LoginUserService, ShowUserService, SortUserService, BlockUserService, \
    UserServiceFacade, CloseUserService
from app.infrastructure.transactions.domain import DepositTransaction, WithdrawTransaction, ExchangeTransaction
from app.infrastructure.transactions.factory import TransactionFactory, TransactionRegistry
from app.infrastructure.transactions.use_cases import TransactionServiceFacade, CreateTransactionService, ShowTransactionService, SortTransactionService
from app.infrastructure.transactions.repository.queries import TransactionQueriesRepository
from app.infrastructure.transactions.repository.commands import TransactionCommandsRepository
from app.infrastructure.wallets.domain import DebitWallet, CreditWallet
from app.infrastructure.wallets.factory import WalletFactory, WalletFactoryRegistry
from app.infrastructure.wallets.repository.mapper import WalletMapper
from app.infrastructure.wallets.use_cases import CreateWalletService, SortWalletService, ShowWalletService, CloseWalletService, \
    WalletServiceFacade, BlockWalletService
from app.infrastructure.wallets.repository.commands import WalletCommandsRepository
from app.infrastructure.wallets.repository.queries import WalletQueriesRepository


def activate_user_factory() -> 'UserFactory':
    user_registrations = UserRegistrations()
    user_registrations.set_registration(UserStatusesEnum.CLIENT, Client)
    user_registrations.set_registration(UserStatusesEnum.ADMIN, Admin)
    return UserFactory(user_registrations)

def activate_wallet_factory() -> 'WalletFactory':
    wallet_registration = WalletFactoryRegistry()
    wallet_registration.set_registration(WalletTypesEnum.DEBIT, DebitWallet)
    wallet_registration.set_registration(WalletTypesEnum.CREDIT, CreditWallet)
    return WalletFactory(wallet_registration)

def activate_transaction_factory() -> 'TransactionFactory':
    transaction_registration = TransactionRegistry()
    transaction_registration.set_registration(TransactionTypesEnum.DEPOSIT, DepositTransaction)
    transaction_registration.set_registration(TransactionTypesEnum.WITHDRAW, WithdrawTransaction)
    transaction_registration.set_registration(TransactionTypesEnum.EXCHANGE, ExchangeTransaction)
    return TransactionFactory(transaction_registration)

def activate_balance_factory() -> 'BalanceFactory':
    balance_registration = BalanceRegistry()
    balance_registration.set_registration(BalanceTypesEnum.REGULAR, RegularBalance)
    balance_registration.set_registration(BalanceTypesEnum.FOREIGN, ForeignBalance)
    return BalanceFactory(balance_registration)


def activate_user_service_facade(user_factory: 'UserFactory', user_commands_repository: 'UserCommandsRepository', user_queries_repository: 'UserQueriesRepository') -> 'UserServiceFacade':

    create_user_service = CreateUserService(user_factory, user_commands_repository)
    login_user_service = LoginUserService(user_queries_repository)
    show_user_service = ShowUserService(user_queries_repository)
    sort_user_service = SortUserService(user_queries_repository)
    block_user_service = BlockUserService(user_queries_repository, user_commands_repository)
    close_user_service = CloseUserService(user_commands_repository, user_queries_repository)
    return UserServiceFacade(create_user_service, login_user_service, show_user_service, block_user_service, sort_user_service, close_user_service)

def activate_wallet_service_facade(wallet_factory: 'WalletFactory', wallet_commands_repository: 'WalletCommandsRepository', wallet_queries_repository: 'WalletQueriesRepository', user_commands_repository: 'UserCommandsRepository'):

    create_wallet_service = CreateWalletService(wallet_factory, wallet_commands_repository, user_commands_repository)
    show_wallet_service = ShowWalletService(wallet_queries_repository)
    sort_wallet_service = SortWalletService(wallet_queries_repository)
    block_wallet_service = BlockWalletService(wallet_commands_repository, wallet_queries_repository)
    close_wallet_service = CloseWalletService(wallet_commands_repository, wallet_queries_repository)
    return WalletServiceFacade(create_wallet_service, show_wallet_service, sort_wallet_service, block_wallet_service, close_wallet_service)

def activate_transaction_service_facade(transaction_factory: 'TransactionFactory', transaction_commands_repository: 'TransactionCommandsRepository', transaction_queries_repository: 'TransactionQueriesRepository') -> 'TransactionServiceFacade':

    create_transaction_service = CreateTransactionService(transaction_factory, transaction_commands_repository)
    show_transaction_service = ShowTransactionService(transaction_queries_repository)
    sort_transaction_service = SortTransactionService(transaction_queries_repository)
    return TransactionServiceFacade(create_transaction_service, show_transaction_service, sort_transaction_service)


def main() -> None:

    add_logger()
    # currencies_zipper = start_currencies_parser()
    # load_currencies_into_enum(currencies_zipper)

    user_factory = activate_user_factory()
    wallet_factory = activate_wallet_factory()
    transaction_factory = activate_transaction_factory()
    balance_factory = activate_balance_factory()

    user_mapper = UserMapper(user_factory)
    wallet_mapper = WalletMapper(wallet_factory)
    transaction_mapper = TransactionMapper(transaction_factory)
    balance_mapper = BalanceMapper(balance_factory)

    user_commands_repository = UserCommandsRepository(session_factory, user_mapper)
    user_queries_repository = UserQueriesRepository(session_factory, user_mapper, wallet_mapper)
    wallet_commands_repository = WalletCommandsRepository(session_factory, wallet_mapper)
    wallet_queries_repository = WalletQueriesRepository(session_factory, wallet_mapper)
    transaction_commands_repository = TransactionCommandsRepository(session_factory, transaction_mapper)
    transaction_queries_repository = TransactionQueriesRepository(session_factory, transaction_mapper)
    balance_commands_repository = BalanceCommandsRepository(session_factory, balance_mapper)
    balance_queries_repository = BalanceQueriesRepository(session_factory, balance_mapper)

    user_service_facade = activate_user_service_facade(user_factory, user_commands_repository, user_queries_repository)
    wallet_service_facade = activate_wallet_service_facade(wallet_factory, wallet_commands_repository, wallet_queries_repository, user_commands_repository)
    transaction_service_facade = activate_transaction_service_facade(transaction_factory, transaction_commands_repository, transaction_queries_repository)




    # user_schema = CreateUserSchema(key=UserStatusesEnum.CLIENT, name='test', email='test@y.ru', password='gk;wjgli7gylbn^')
    # user = user_service_facade.create_user(user_schema)
    # login_schema = LoginUserSchema(email='test@y.ru', password='gk;wjgli7gylbn^')
    # user = user_service_facade.login_user(login_schema)
    # print(user)

    # wallets = user_queries_repository.select_my_wallets(user)
    # for w in wallets:
    #     print(w)
    #     print('\n')

    # wallet_schema = CreateWalletSchema(key=WalletTypesEnum.CREDIT, pin='1234')
    # wallet = wallet_service_facade.create_wallet(user, wallet_schema)
    # print(wallet)
    # wqr = WalletQueriesRepository(session_factory, wallet_mapper)
    # print(wqr.select_my_wallets(user))


if __name__ == '__main__':
    main()