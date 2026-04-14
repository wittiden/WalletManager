from app.common.enums.transaction_enums import TransactionTypesEnum
from app.common.enums.user_enums import UserStatusesEnum
from app.common.enums.wallet_enums import WalletTypesEnum
from app.core.logger import add_logger
from app.parsers.currencies_parser import start_currencies_parser
from app.users.domain import Client, Admin
from app.users.factory import UserRegistrations, UserFactory
from app.users.repository.commands import UserCommandsRepository
from app.database.engine import session_factory
from app.users.repository.queries import UserQueriesRepository
from app.users.use_cases import CreateUserService, LoginUserService, ShowUserService, SortUserService, BlockUserService, \
    UserServiceFacade
from app.transactions.domain import DepositTransaction, WithdrawTransaction, ExchangeTransaction
from app.transactions.factory import TransactionFactory, TransactionRegistry
from app.transactions.use_cases import TransactionServiceFacade, CreateTransactionService, ShowTransactionService, SortTransactionService
from app.transactions.repository.queries import TransactionQueriesRepository
from app.transactions.repository.commands import TransactionCommandsRepository
from app.wallets.domain import ForeignWallet, RegularWallet
from app.wallets.factory import WalletFactory, WalletFactoryRegistry
from app.wallets.use_cases import CreateWalletService, SortWalletService, ShowWalletService, CloseWalletService, \
    WalletServiceFacade, BlockWalletService, WalletOperationsServiceFacade, DepositWalletOperationService, WithdrawWalletOperationService, ExchangeWalletOperationService
from app.wallets.repository.queries import WalletQueriesRepository
from app.wallets.repository.commands import WalletCommandsRepository


def main() -> None:

    add_logger()
    start_currencies_parser()


    user_commands_repository = UserCommandsRepository(session_factory)
    user_queries_repository = UserQueriesRepository(session_factory)

    user_registrations = UserRegistrations()
    user_registrations.set_registration(UserStatusesEnum.CLIENT, Client)
    user_registrations.set_registration(UserStatusesEnum.ADMIN, Admin)
    user_factory = UserFactory(user_registrations)

    create_user_service = CreateUserService(user_factory, user_commands_repository)
    login_user_service = LoginUserService(user_queries_repository)
    show_user_service = ShowUserService(user_queries_repository)
    sort_user_service = SortUserService(user_queries_repository)
    block_user_service = BlockUserService(user_queries_repository, user_commands_repository)
    user_service_facade = UserServiceFacade(create_user_service, login_user_service, show_user_service, block_user_service, sort_user_service)


    transaction_commands_repository = TransactionCommandsRepository(session_factory)
    transaction_queries_repository = TransactionQueriesRepository(session_factory)

    transaction_registration = TransactionRegistry()
    transaction_registration.set_registration(TransactionTypesEnum.DEPOSIT, DepositTransaction)
    transaction_registration.set_registration(TransactionTypesEnum.WITHDRAW, WithdrawTransaction)
    transaction_registration.set_registration(TransactionTypesEnum.EXCHANGE, ExchangeTransaction)
    transaction_factory = TransactionFactory(transaction_registration)

    create_transaction_service = CreateTransactionService(transaction_factory, transaction_commands_repository)
    show_transaction_service = ShowTransactionService(transaction_queries_repository)
    sort_transaction_service = SortTransactionService(transaction_queries_repository)
    transaction_service_facade = TransactionServiceFacade(create_transaction_service, show_transaction_service, sort_transaction_service)


    wallet_commands_repository = WalletCommandsRepository(session_factory)
    wallet_queries_repository = WalletQueriesRepository(session_factory)

    wallet_registration = WalletFactoryRegistry()
    wallet_registration.set_registration(WalletTypesEnum.REGULAR, RegularWallet)
    wallet_registration.set_registration(WalletTypesEnum.FOREIGN, ForeignWallet)
    wallet_factory = WalletFactory(wallet_registration)

    create_wallet_service = CreateWalletService(wallet_factory, wallet_commands_repository)
    show_wallet_service = ShowWalletService(wallet_queries_repository)
    sort_wallet_service = SortWalletService(wallet_queries_repository)
    block_wallet_service = BlockWalletService(wallet_commands_repository, wallet_queries_repository)
    close_wallet_service = CloseWalletService(wallet_commands_repository, wallet_queries_repository)
    wallet_service_facade = WalletServiceFacade(create_wallet_service, show_wallet_service, sort_wallet_service, block_wallet_service, close_wallet_service)

    deposit_wallet_operation_service = DepositWalletOperationService()
    withdraw_wallet_operation_service = WithdrawWalletOperationService()
    exchange_wallet_operation_service = ExchangeWalletOperationService()
    wallet_operations_service_facade = WalletOperationsServiceFacade(deposit_wallet_operation_service, withdraw_wallet_operation_service, exchange_wallet_operation_service)




if __name__ == '__main__':
    main()