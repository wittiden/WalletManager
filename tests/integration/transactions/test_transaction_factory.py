import pytest

from app.infrastructure.transactions.factory import TransactionFactory


class TestTransactionFactory:
    """Класс для тестирования фабрики транзакций"""

    @pytest.mark.integration
    def test_create_deposit_transaction(self, container, sample_transaction_deposit):
        transaction_factory = container.get(TransactionFactory)

        transaction = transaction_factory.create_transaction(sample_transaction_deposit.operation_type, sample_transaction_deposit.from_address, sample_transaction_deposit.to_address, sample_transaction_deposit.completed_at, sample_transaction_deposit.amount, sample_transaction_deposit.operation_status)

        assert transaction.operation_type == sample_transaction_deposit.operation_type
        assert transaction.operation_status == sample_transaction_deposit.operation_status
        assert transaction.from_address == sample_transaction_deposit.from_address
        assert transaction.to_address == sample_transaction_deposit.to_address
        assert transaction.completed_at == sample_transaction_deposit.completed_at
        assert transaction.amount == sample_transaction_deposit.amount

    @pytest.mark.integration
    def test_create_withdraw_transaction(self, container, sample_transaction_withdraw):
        transaction_factory = container.get(TransactionFactory)

        transaction = transaction_factory.create_transaction(sample_transaction_withdraw.operation_type, sample_transaction_withdraw.from_address, sample_transaction_withdraw.to_address, sample_transaction_withdraw.completed_at, sample_transaction_withdraw.amount, sample_transaction_withdraw.operation_status, sample_transaction_withdraw.withdraw_fee)

        assert transaction.operation_type == sample_transaction_withdraw.operation_type
        assert transaction.operation_status == sample_transaction_withdraw.operation_status
        assert transaction.from_address == sample_transaction_withdraw.from_address
        assert transaction.to_address == sample_transaction_withdraw.to_address
        assert transaction.completed_at == sample_transaction_withdraw.completed_at
        assert transaction.amount == sample_transaction_withdraw.amount
        assert transaction.withdraw_fee == sample_transaction_withdraw.withdraw_fee

    @pytest.mark.integration
    def test_create_exchange_transaction(self, container, sample_transaction_exchange):
        transaction_factory = container.get(TransactionFactory)

        transaction = transaction_factory.create_transaction(sample_transaction_exchange.operation_type, sample_transaction_exchange.from_address, sample_transaction_exchange.to_address, sample_transaction_exchange.completed_at, sample_transaction_exchange.amount, sample_transaction_exchange.operation_status, sample_transaction_exchange.exchange_fee, sample_transaction_exchange.from_currency, sample_transaction_exchange.to_currency)

        assert transaction.operation_type == sample_transaction_exchange.operation_type
        assert transaction.operation_status == sample_transaction_exchange.operation_status
        assert transaction.from_address == sample_transaction_exchange.from_address
        assert transaction.to_address == sample_transaction_exchange.to_address
        assert transaction.completed_at == sample_transaction_exchange.completed_at
        assert transaction.amount == sample_transaction_exchange.amount
        assert transaction.exchange_fee == sample_transaction_exchange.exchange_fee
        assert transaction.from_currency == sample_transaction_exchange.from_currency
        assert transaction.to_currency == sample_transaction_exchange.to_currency