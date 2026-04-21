from decimal import Decimal

import pytest

from app.common.enums.transaction_enums import TransactionTypesEnum
from app.infrastructure.transactions.schemas import CreateDepositOrWithdrawTransactionSchema, CreateExchangeTransactionSchema
from app.infrastructure.transactions.use_cases import TransactionServiceFacade


class TestTransactionServiceFacade:
    """Класс для тестирования работы фасада операций над транзакциями"""

    @pytest.mark.integration
    @pytest.mark.parametrize(
        'currency, from_address, to_address, amount, fee, operation_type',
        [
            ('USD', '12345678909876543210987654', '12345678909876543210987654', Decimal(20), Decimal(1.001), TransactionTypesEnum.DEPOSIT),
            ('AED', '12345678909876543210987654', '12345678909876543210987654', Decimal(5), Decimal(1.002), TransactionTypesEnum.WITHDRAW),
        ],
    )
    def test_create_deposit_or_withdraw_transaction_good(self, container, currency, from_address, to_address, amount, fee, operation_type):
        facade = container.get(TransactionServiceFacade)

        schema = CreateDepositOrWithdrawTransactionSchema(
            currency=currency, from_address=from_address, to_address=to_address, amount=amount, fee=fee, operation_type=operation_type
        )
        transaction = facade.create_transaction(schema)

        assert transaction.currency == currency
        assert transaction.from_address == from_address
        assert transaction.to_address == to_address
        assert transaction.amount == amount
        assert transaction.fee == fee
        assert transaction.operation_type == operation_type

    @pytest.mark.integration
    @pytest.mark.parametrize(
        'from_address, to_address, amount, fee, operation_type, from_currency, to_currency, rate',
        [
            ('12345678909876543210987654', '12345678909876543210987654', Decimal(20), Decimal(1.001), TransactionTypesEnum.EXCHANGE, 'BYN', 'USD', Decimal(2.8)),
        ],
    )
    def test_create_exchange_transaction_good(self, container, from_address, to_address, amount, fee, operation_type, from_currency, to_currency, rate):
        facade = container.get(TransactionServiceFacade)

        schema = CreateExchangeTransactionSchema(
            from_address=from_address, to_address=to_address, amount=amount, fee=fee, operation_type=operation_type, from_currency=from_currency, to_currency=to_currency, rate=rate
        )
        transaction = facade.create_transaction(schema)

        assert transaction.from_address == from_address
        assert transaction.to_address == to_address
        assert transaction.amount == amount
        assert transaction.fee == fee
        assert transaction.operation_type == operation_type
        assert transaction.from_currency == from_currency
        assert transaction.to_currency == to_currency
        assert transaction.rate == rate

    @pytest.mark.integration
    def test_show_transaction_good(self, container, sample_transaction_deposit):
        facade = container.get(TransactionServiceFacade)

        transaction = facade.create_transaction(sample_transaction_deposit)

        find_transaction = facade.show_transaction(transaction.item_id)
        assert transaction.from_address == find_transaction.from_address
        assert transaction.to_address == find_transaction.to_address
        assert transaction.amount == find_transaction.amount
        assert transaction.fee == find_transaction.fee
        assert transaction.operation_type == find_transaction.operation_type
        assert transaction.currency == find_transaction.currency
