import pytest

from app.common.enums.balance_enums import WalletBalanceCurrenciesEnum
from app.parsers.currencies_parser import start_currencies_parser, load_currencies_into_enum


class TestCurrencyParser:
    """Класс для тестирования работы парсера типов валют"""

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.timeout(10)
    def test_start_currency_parser(self):
        result = start_currencies_parser()

        assert isinstance(result, list)
        assert len(result) > 20

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.timeout(10)
    def test_load_currencies_into_enum(self):
        currencies_zip = start_currencies_parser()
        load_currencies_into_enum(currencies_zip)

        assert len(WalletBalanceCurrenciesEnum) > len(currencies_zip)