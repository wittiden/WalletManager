from decimal import Decimal

import pytest
from pytest_mock import MockerFixture

from app.infrastructure.balances.domain import ForeignBalance, RegularBalance


class TestBalanceDomain:
    """Класс для тестирования домена баланса"""

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'wallet_id, amount, currency',
        [
            ('wallet_id', Decimal(10), 'USD'),
        ],
    )
    def test_regular_balance_good(self, wallet_id, amount, currency):
        balance = RegularBalance(wallet_id, amount, currency)

        assert balance.wallet_id == wallet_id
        assert balance.amount == amount
        assert balance.currency == currency

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'wallet_id, amounts, currencies',
        [
            ('wallet_id', [Decimal(1), Decimal(3), Decimal(10)], ['USD', 'BYN', 'RUB']),
        ],
    )
    def test_foreign_balance_good(self, wallet_id, amounts, currencies):
        balance = ForeignBalance(wallet_id, amounts, currencies)

        assert balance.wallet_id == wallet_id
        assert balance.amounts == amounts
        assert balance.currencies == currencies

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'wallet_id, amount, currency',
        [
            ('', Decimal(10), 'USD'),
            ('wallet_id', Decimal(-10), 'USD'),
            ('wallet_id', Decimal(10), ''),
        ],
    )
    def test_regular_balance_bad(self, wallet_id, amount, currency):
        with pytest.raises(ValueError):
            RegularBalance(wallet_id, amount, currency)

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'wallet_id, amounts, currencies',
        [
            ('wallet_id', [], ['USD', 'BYN', 'RUB']),
            ('wallet_id', [Decimal(1), Decimal(3), Decimal(10)], []),
        ],
    )
    def test_foreign_balance_bad(self, wallet_id, amounts, currencies):
        with pytest.raises(ValueError):
            ForeignBalance(wallet_id, amounts, currencies)

    @pytest.mark.unit
    def test_balance_setter(self, mocker: MockerFixture, sample_balance_base):
        mock = mocker.patch('app.infrastructure.balances.domain.upgrade_balance_signal.send')

        sample_balance_base.wallet_id = 'new_wallet_id'

        assert mock.call_count == 1
