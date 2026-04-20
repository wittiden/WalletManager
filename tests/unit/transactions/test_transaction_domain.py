from datetime import datetime
from decimal import Decimal
import pytest

from app.common.enums.transaction_enums import TransactionStatusesEnum, TransactionTypesEnum
from app.infrastructure.transactions.domain import DepositTransaction, WithdrawTransaction, \
    ExchangeTransaction


class TestTransactionDomain:
    """Класс для тестирования домена транзакций"""

    @pytest.mark.unit
    @pytest.mark.parametrize('from_address, to_address, completed_at, amount, operation_status, operation_type', [
        ('12345', '54321', datetime.now(), Decimal(1), TransactionStatusesEnum.PENDING, TransactionTypesEnum.DEPOSIT),
    ])
    def test_deposit_transaction_good(self, from_address, to_address, completed_at, amount, operation_status, operation_type):
        transaction = DepositTransaction(from_address, to_address, completed_at, amount, operation_status)

        assert transaction.from_address == from_address
        assert transaction.to_address == to_address
        assert transaction.completed_at == completed_at
        assert transaction.amount == amount
        assert transaction.operation_status == operation_status

    @pytest.mark.unit
    @pytest.mark.parametrize('from_address, to_address, completed_at, amount, operation_status, operation_type, fee', [
        ('12345', '54321', datetime.now(), Decimal(1), TransactionStatusesEnum.FAILED, TransactionTypesEnum.WITHDRAW, Decimal(0.3)),
    ])
    def test_withdraw_transaction_good(self, from_address, to_address, completed_at, amount, operation_status, operation_type, fee):
        transaction = WithdrawTransaction(from_address, to_address, completed_at, amount, operation_status, fee)

        assert transaction.from_address == from_address
        assert transaction.to_address == to_address
        assert transaction.completed_at == completed_at
        assert transaction.amount == amount
        assert transaction.withdraw_fee == fee
        assert transaction.operation_status == operation_status

    @pytest.mark.unit
    @pytest.mark.parametrize('from_address, to_address, completed_at, amount, operation_status, operation_type, fee, from_currency, to_currency', [
        ('12345', '54321', datetime.now(), Decimal(1), TransactionStatusesEnum.FAILED, TransactionTypesEnum.WITHDRAW, Decimal(0.3), 'USD', 'EUR'),
    ])
    def test_exchange_transaction_good(self, from_address, to_address, completed_at, amount, operation_status, operation_type, fee, from_currency, to_currency):
        transaction = ExchangeTransaction(from_address, to_address, completed_at, amount, operation_status, fee, from_currency, to_currency)

        assert transaction.from_address == from_address
        assert transaction.to_address == to_address
        assert transaction.completed_at == completed_at
        assert transaction.amount == amount
        assert transaction.exchange_fee == fee
        assert transaction.from_currency == from_currency
        assert transaction.to_currency == to_currency
        assert transaction.operation_status == operation_status

    @pytest.mark.unit
    @pytest.mark.parametrize('from_address, to_address, completed_at, amount, operation_status, operation_type', [
        ('', '54321', datetime.now(), Decimal(1), TransactionStatusesEnum.PENDING, TransactionTypesEnum.DEPOSIT),
        ('12345', '', datetime.now(), Decimal(1), TransactionStatusesEnum.PENDING, TransactionTypesEnum.DEPOSIT),
        ('12345', '54321', '', Decimal(1), TransactionStatusesEnum.PENDING, TransactionTypesEnum.DEPOSIT),
        ('12345', '54321', datetime.now(), Decimal(-1), TransactionStatusesEnum.PENDING, TransactionTypesEnum.DEPOSIT),
        ('12345', '54321', datetime.now(), Decimal(1), '', TransactionTypesEnum.DEPOSIT),
    ])
    def test_deposit_transaction_bad(self, from_address, to_address, completed_at, amount, operation_status, operation_type):
        with pytest.raises(ValueError):
            DepositTransaction(from_address, to_address, completed_at, amount, operation_status)


    @pytest.mark.unit
    @pytest.mark.parametrize('from_address, to_address, completed_at, amount, operation_status, operation_type, fee', [
        ('12345', '54321', datetime.now(), Decimal(1), TransactionStatusesEnum.PENDING, TransactionTypesEnum.DEPOSIT, Decimal(-0.2)),
    ])
    def test_withdraw_transaction_bad(self, from_address, to_address, completed_at, amount, operation_status, operation_type, fee):
        with pytest.raises(ValueError):
            WithdrawTransaction(from_address, to_address, completed_at, amount, operation_status, fee)

    @pytest.mark.unit
    @pytest.mark.parametrize('from_address, to_address, completed_at, amount, operation_status, operation_type, fee, from_currency, to_currency', [
        ('12345', '54321', datetime.now(), Decimal(1), TransactionStatusesEnum.PENDING, TransactionTypesEnum.DEPOSIT, Decimal(0.2), '', 'BYN'),
        ('12345', '54321', datetime.now(), Decimal(1), TransactionStatusesEnum.PENDING, TransactionTypesEnum.DEPOSIT, Decimal(0.2), 'USD', ''),
    ])
    def test_withdraw_transaction_bad(self, from_address, to_address, completed_at, amount, operation_status, operation_type, fee, from_currency, to_currency):
        with pytest.raises(ValueError):
            ExchangeTransaction(from_address, to_address, completed_at, amount, operation_status, fee, from_currency, to_currency)