from app.core.logger import add_logger
from app.parsers.currencies_parser import start_currencies_parser
from app.users.domain import Admin, Client
from app.users.factory import UserFactory, UserRegistrations
from app.users.use_cases import UserServiceFacade, CreateUserService, LoginUserService, SortUserService, ShowUserService, BlockUserService
from app.common.enums.user_enums import UserStatusesEnum
from app.users.repository.repository import UserRepository
from app.wallets.domain import RegularWallet, ForeignWallet
from app.wallets.factory import WalletFactory, WalletFactoryRegistry
from app.wallets.repository.repository import WalletRepository
from app.common.enums.wallet_enums import WalletTypesEnum
from app.wallets.use_cases import CreateWalletService, ShowWalletService, SortWalletService, BlockWalletService, CloseWalletService, WalletServiceFacade, WalletOperationsFacade, WithdrawWalletOperationService, DepositWalletOperationService, ExchangeWalletOperationService


def main() -> None:

    add_logger()
    start_currencies_parser()

    user_repository = UserRepository()

    user_registrations = UserRegistrations()
    user_registrations.set_registration(UserStatusesEnum.CLIENT, Client)
    user_registrations.set_registration(UserStatusesEnum.ADMIN, Admin)
    user_factory = UserFactory(user_registrations)

    create_user_service = CreateUserService(user_repository, user_factory)
    login_user_service = LoginUserService(user_repository)
    show_user_service = ShowUserService(user_repository)
    sort_user_service = SortUserService(user_repository)
    block_user_service = BlockUserService(user_repository)
    user_service_facade = UserServiceFacade(create_user_service, login_user_service, show_user_service, block_user_service, sort_user_service)

    wallet_repository = WalletRepository()

    wallet_registrations = WalletFactoryRegistry()
    wallet_registrations.set_registration(WalletTypesEnum.REGULAR, RegularWallet)
    wallet_registrations.set_registration(WalletTypesEnum.FOREIGN, ForeignWallet)
    wallet_factory = WalletFactory(wallet_registrations)

    create_wallet_service = CreateWalletService(wallet_repository, wallet_factory)
    show_wallet_service = ShowWalletService(wallet_repository)
    sort_wallet_service = SortWalletService(wallet_repository)
    block_wallet_service = BlockWalletService(wallet_repository)
    close_wallet_service = CloseWalletService(wallet_repository)
    wallet_service_facade = WalletServiceFacade(create_wallet_service, show_wallet_service, sort_wallet_service, block_wallet_service, close_wallet_service)

    withdraw_wallet_operation_service = WithdrawWalletOperationService()
    deposit_wallet_operation_service = DepositWalletOperationService()
    exchange_wallet_operation_service = ExchangeWalletOperationService()
    wallet_operations_facade = WalletOperationsFacade(deposit_wallet_operation_service, withdraw_wallet_operation_service, exchange_wallet_operation_service)




if __name__ == '__main__':
    main()