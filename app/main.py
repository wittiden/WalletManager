from app.core.logger import add_logger
from app.infrastructure.balances.use_cases import BalanceServiceFacade
from app.infrastructure.transactions.use_cases import TransactionServiceFacade
from app.infrastructure.users.use_cases import UserServiceFacade
from app.infrastructure.wallets.use_cases import WalletServiceFacade
from app.parsers.currencies_name_parser import load_currencies_name_into_enum, start_currencies_name_parser
from app.di.container import build_container


def main() -> None:

    add_logger()

    currencies_zipper = start_currencies_name_parser()
    load_currencies_name_into_enum(currencies_zipper)

    container = build_container()
    user_service_facade = container.get(UserServiceFacade)
    wallet_service_facade = container.get(WalletServiceFacade)
    balance_service_facade = container.get(BalanceServiceFacade)
    transaction_service_facade = container.get(TransactionServiceFacade)


if __name__ == '__main__':
    main()