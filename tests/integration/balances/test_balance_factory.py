import pytest

from app.infrastructure.balances.factory import BalanceFactory


class TestBalanceFactory:
    """Класс для тестирования фабрики балансов"""

    @pytest.mark.integration
    def test_create_regular_balance(self, container, sample_balance_regular):
        balance_factory = container.get(BalanceFactory)

        balance = balance_factory.create_balance(sample_balance_regular.balance_type, sample_balance_regular.wallet_id, sample_balance_regular.amount, sample_balance_regular.currency)

        assert balance.balance_type == sample_balance_regular.balance_type
        assert balance.wallet_id == sample_balance_regular.wallet_id
        assert balance.amount == sample_balance_regular.amount
        assert balance.currency == sample_balance_regular.currency

    @pytest.mark.integration
    def test_create_foreign_balance(self, container, sample_balance_foreign):
        balance_factory = container.get(BalanceFactory)

        balance = balance_factory.create_balance(sample_balance_foreign.balance_type, sample_balance_foreign.wallet_id, sample_balance_foreign.amounts, sample_balance_foreign.currencies)

        assert balance.balance_type == sample_balance_foreign.balance_type
        assert balance.wallet_id == sample_balance_foreign.wallet_id
        assert balance.amounts == sample_balance_foreign.amounts
        assert balance.currencies == sample_balance_foreign.currencies