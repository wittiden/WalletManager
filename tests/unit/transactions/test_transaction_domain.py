from datetime import datetime
from decimal import Decimal

import pytest

from app.common.enums.transaction_enums import TransactionTypesEnum
from app.infrastructure.transactions.domain import DepositTransaction, ExchangeTransaction, WithdrawTransaction


class TestTransactionDomain:
    """Класс для тестирования домена транзакций"""

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'from_address, to_address, completed_at, amount, fee, operation_type, currency',
        [
            ('12345', '54321', datetime.now(), Decimal(1), Decimal(0), TransactionTypesEnum.DEPOSIT, 'USD'),
        ],
    )
    def test_deposit_transaction_good(self, from_address, to_address, completed_at, amount, fee, operation_type, currency):
        transaction = DepositTransaction(from_address, to_address, completed_at, amount, fee, currency)

        assert transaction.from_address == from_address
        assert transaction.to_address == to_address
        assert transaction.completed_at == completed_at
        assert transaction.amount == amount
        assert transaction.fee == fee
        assert transaction.currency == currency

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'from_address, to_address, completed_at, amount, fee, operation_type, currency',
        [
            ('12345', '54321', datetime.now(), Decimal(1), Decimal(0.3), TransactionTypesEnum.WITHDRAW, 'AED'),
        ],
    )
    def test_withdraw_transaction_good(self, from_address, to_address, completed_at, amount, fee, operation_type, currency):
        transaction = WithdrawTransaction(from_address, to_address, completed_at, amount, fee, currency)

        assert transaction.from_address == from_address
        assert transaction.to_address == to_address
        assert transaction.completed_at == completed_at
        assert transaction.amount == amount
        assert transaction.fee == fee
        assert transaction.currency == currency

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'from_address, to_address, completed_at, amount, fee, operation_type, from_currency, to_currency, rate',
        [
            ('12345', '54321', datetime.now(), Decimal(1), Decimal(0.3), TransactionTypesEnum.WITHDRAW, 'USD', 'EUR', Decimal(10.9)),
        ],
    )
    def test_exchange_transaction_good(self, from_address, to_address, completed_at, amount, operation_type, fee, from_currency, to_currency, rate):
        transaction = ExchangeTransaction(from_address, to_address, completed_at, amount, fee, from_currency, to_currency, rate)

        assert transaction.from_address == from_address
        assert transaction.to_address == to_address
        assert transaction.completed_at == completed_at
        assert transaction.amount == amount
        assert transaction.fee == fee
        assert transaction.from_currency == from_currency
        assert transaction.to_currency == to_currency
        assert transaction.rate == rate

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'from_address, to_address, completed_at, amount, fee, operation_type, currency',
        [
            ('', '54321', datetime.now(), Decimal(1), Decimal(0), TransactionTypesEnum.DEPOSIT, 'USD'),
            ('12345', '', datetime.now(), Decimal(1), Decimal(0), TransactionTypesEnum.DEPOSIT, 'USD'),
            ('12345', '54321', '', Decimal(1), Decimal(0), TransactionTypesEnum.DEPOSIT, 'USD'),
            ('12345', '54321', datetime.now(), Decimal(-1), Decimal(0), TransactionTypesEnum.DEPOSIT, 'USD'),
            ('12345', '54321', datetime.now(), Decimal(1), Decimal(-1), TransactionTypesEnum.DEPOSIT, 'USD'),
            ('12345', '54321', datetime.now(), Decimal(1), Decimal(0), TransactionTypesEnum.DEPOSIT, ''),
        ],
    )
    def test_deposit_and_withdraw_transaction_bad(self, from_address, to_address, completed_at, amount, fee, operation_type, currency):
        with pytest.raises(ValueError):
            DepositTransaction(from_address, to_address, completed_at, amount, fee, currency)

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'from_address, to_address, completed_at, amount, fee, operation_type, from_currency, to_currency, rate',
        [
            ('12345', '54321', datetime.now(), Decimal(1), Decimal(0.2), TransactionTypesEnum.DEPOSIT, '', 'BYN', Decimal(3.02)),
            ('12345', '54321', datetime.now(), Decimal(1), Decimal(0.2), TransactionTypesEnum.DEPOSIT, 'USD', '', Decimal(3.02)),
            ('12345', '54321', datetime.now(), Decimal(1), Decimal(0.2), TransactionTypesEnum.DEPOSIT, 'USD', 'BYN', Decimal(-3.02)),
        ],
    )
    def test_exchange_transaction_bad(self, from_address, to_address, completed_at, amount, operation_type, fee, from_currency, to_currency, rate):
        with pytest.raises(ValueError):
            ExchangeTransaction(from_address, to_address, completed_at, amount, fee, from_currency, to_currency, rate)
