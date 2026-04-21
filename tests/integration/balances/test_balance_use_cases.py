from decimal import Decimal

import pytest

from app.common.enums.balance_enums import BalanceTypesEnum
from app.common.enums.transaction_enums import TransactionTypesEnum
from app.infrastructure.balances.schemas import CreateRegularBalanceSchema, CreateForeignBalanceSchema
from app.infrastructure.balances.use_cases import BalanceServiceFacade, BalanceOperationsServiceFacade
from app.infrastructure.transactions.schemas import CreateDepositOrWithdrawTransactionSchema
from app.infrastructure.transactions.use_cases import TransactionServiceFacade


class TestBalanceServiceFacade:
    """Класс для тестирования работы фасада операций над балансом"""

    @pytest.mark.integration
    @pytest.mark.parametrize('key, amount, currency', [
        (BalanceTypesEnum.REGULAR, Decimal(10), 'USD'),
    ])
    def test_create_regular_balance_good(self, container, load_client_and_wallet_to_db, key, amount, currency):
        facade = container.get(BalanceServiceFacade)

        wallet = load_client_and_wallet_to_db

        schema = CreateRegularBalanceSchema(key=key, amount=amount, currency=currency)
        balance = facade.create_balance(wallet, schema)

        assert balance.wallet_id == wallet.item_id
        assert balance.currency == currency
        assert balance.amount == amount
        assert balance.balance_type == key

    @pytest.mark.integration
    @pytest.mark.parametrize('key, amounts, currencies', [
        (BalanceTypesEnum.FOREIGN, [Decimal(10), Decimal(5), Decimal(3)], ['USD', 'BYN', 'EUR']),
    ])
    def test_create_foreign_balance_good(self, container, load_client_and_wallet_to_db, key, amounts, currencies):
        facade = container.get(BalanceServiceFacade)

        wallet = load_client_and_wallet_to_db

        schema = CreateForeignBalanceSchema(key=key, amounts=amounts, currencies=currencies)
        balance = facade.create_balance(wallet, schema)

        assert balance.wallet_id == wallet.item_id
        assert balance.currencies == currencies
        assert balance.amounts == amounts
        assert balance.balance_type == key

    @pytest.mark.integration
    def test_show_regular_balance(self, container, load_client_and_wallet_to_db, sample_regular_balance):
        facade = container.get(BalanceServiceFacade)

        wallet = load_client_and_wallet_to_db

        balance = facade.create_balance(wallet, sample_regular_balance)

        find_balance = facade.show_regular_balance(wallet)

        assert find_balance.wallet_id == balance.wallet_id
        assert find_balance.balance_type == balance.balance_type
        assert find_balance.currency == balance.currency
        assert find_balance.amount == balance.amount

    @pytest.mark.integration
    def test_show_foreign_balances(self, container, load_client_and_wallet_to_db, sample_foreign_balance):
        facade = container.get(BalanceServiceFacade)

        wallet = load_client_and_wallet_to_db

        balance = facade.create_balance(wallet, sample_foreign_balance)

        find_balances = facade.show_foreign_balance(wallet)

        assert find_balances.wallet_id == balance.wallet_id
        assert find_balances.balance_type == balance.balance_type
        assert find_balances.currencies == balance.currencies
        assert find_balances.amounts == balance.amounts

    @pytest.mark.integration
    def test_freeze_regular_balance_good(self, container, load_client_and_wallet_to_db, sample_regular_balance, load_admin_to_db):
        facade = container.get(BalanceServiceFacade)

        wallet = load_client_and_wallet_to_db
        admin = load_admin_to_db

        balance = facade.create_balance(wallet, sample_regular_balance)

        facade.freeze_regular_balance(admin, wallet.item_id)

        find_balance = facade.show_regular_balance(wallet)
        print(find_balance)

        assert find_balance.wallet_id == balance.wallet_id
        assert find_balance.balance_type == balance.balance_type
        assert find_balance.currency == balance.currency
        assert find_balance.amount == balance.amount
        assert find_balance.is_frozen is True

    @pytest.mark.integration
    def test_freeze_foreign_balance_good(self, container, load_client_and_wallet_to_db, sample_foreign_balance, load_admin_to_db):
        facade = container.get(BalanceServiceFacade)

        wallet = load_client_and_wallet_to_db
        admin = load_admin_to_db

        balance = facade.create_balance(wallet, sample_foreign_balance)

        facade.freeze_foreign_balance(admin, wallet.item_id)

        find_balances = facade.show_foreign_balance(wallet)

        assert find_balances.wallet_id == balance.wallet_id
        assert find_balances.balance_type == balance.balance_type
        assert find_balances.currencies == balance.currencies
        assert find_balances.amounts == balance.amounts
        assert find_balances.is_frozen is True

    @pytest.mark.integration
    def test_unfreeze_regular_balance_good(self, container, load_client_and_wallet_to_db, sample_regular_balance, load_admin_to_db):
        facade = container.get(BalanceServiceFacade)

        wallet = load_client_and_wallet_to_db
        admin = load_admin_to_db

        balance = facade.create_balance(wallet, sample_regular_balance)

        facade.freeze_regular_balance(admin, wallet.item_id)
        facade.unfreeze_regular_balance(admin, wallet.item_id)

        find_balance = facade.show_regular_balance(wallet)
        print(find_balance)

        assert find_balance.wallet_id == balance.wallet_id
        assert find_balance.balance_type == balance.balance_type
        assert find_balance.currency == balance.currency
        assert find_balance.amount == balance.amount
        assert find_balance.is_frozen is False

    @pytest.mark.integration
    def test_unfreeze_foreign_balance_good(self, container, load_client_and_wallet_to_db, sample_foreign_balance, load_admin_to_db):
        facade = container.get(BalanceServiceFacade)

        wallet = load_client_and_wallet_to_db
        admin = load_admin_to_db

        balance = facade.create_balance(wallet, sample_foreign_balance)

        facade.freeze_foreign_balance(admin, wallet.item_id)
        facade.unfreeze_foreign_balance(admin, wallet.item_id)

        find_balances = facade.show_foreign_balance(wallet)

        assert find_balances.wallet_id == balance.wallet_id
        assert find_balances.balance_type == balance.balance_type
        assert find_balances.currencies == balance.currencies
        assert find_balances.amounts == balance.amounts
        assert find_balances.is_frozen is False


class TestBalanceOperationsServiceFacade:
    """Класс для тестирования работы фасада операций пополнения и снятия над балансом"""

    @pytest.mark.integration
    def test_deposit_balance_good(self, container, load_client_and_wallet_to_db, sample_regular_balance):
        balance_facade = container.get(BalanceServiceFacade)
        operations_facade = container.get(BalanceOperationsServiceFacade)
        transaction_facade = container.get(TransactionServiceFacade)

        wallet = load_client_and_wallet_to_db

        balance = balance_facade.create_balance(wallet, sample_regular_balance)

        transaction_schema = CreateDepositOrWithdrawTransactionSchema(currency=balance.currency, from_address=wallet.address, to_address=wallet.address, amount=Decimal(100), fee=Decimal(1.02), operation_type=TransactionTypesEnum.DEPOSIT)
        transaction = transaction_facade.create_transaction(transaction_schema)
        operations_facade.deposit_balance(balance, transaction)

    @pytest.mark.integration
    def test_withdraw_balance_good(self, container, load_client_and_wallet_to_db, sample_regular_balance):
        balance_facade = container.get(BalanceServiceFacade)
        operations_facade = container.get(BalanceOperationsServiceFacade)
        transaction_facade = container.get(TransactionServiceFacade)

        wallet = load_client_and_wallet_to_db

        balance = balance_facade.create_balance(wallet, sample_regular_balance)

        transaction_schema = CreateDepositOrWithdrawTransactionSchema(currency=balance.currency,from_address=wallet.address, to_address=wallet.address, amount=Decimal(10), fee=Decimal(1.02), operation_type=TransactionTypesEnum.WITHDRAW)
        transaction = transaction_facade.create_transaction(transaction_schema)
        operations_facade.withdraw_balance(balance, transaction)