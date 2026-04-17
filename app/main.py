from app.core.logger import add_logger
from app.infrastructure.balances.use_cases import BalanceServiceFacade
from app.infrastructure.transactions.use_cases import TransactionServiceFacade
from app.infrastructure.users.use_cases import UserServiceFacade
from app.infrastructure.wallets.use_cases import WalletServiceFacade
from app.parsers.currencies_parser import load_currencies_into_enum, start_currencies_parser
from app.di.container import container


def main() -> None:

    add_logger()
    currencies_zipper = start_currencies_parser()
    load_currencies_into_enum(currencies_zipper)

    with container() as ctx:
        user_facade = ctx.get(UserServiceFacade)
        wallet_facade = ctx.get(WalletServiceFacade)
        balance_facade = ctx.get(BalanceServiceFacade)
        transaction_facade = ctx.get(TransactionServiceFacade)


if __name__ == '__main__':
    main()