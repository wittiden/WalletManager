import requests
from bs4 import BeautifulSoup
import fake_useragent
from aenum import extend_enum

from app.common.enums.wallet_enums import WalletBalanceCurrenciesEnum
from app.core.exceptions import WebElementNotFoundError


def start_currencies_parser() -> list:
    link = 'https://myfin.by/converter'
    user_agent = fake_useragent.FakeUserAgent().random

    header = {'user-agent': user_agent}

    response = requests.get(link, headers=header)
    if response:
        soup = BeautifulSoup(response.text, 'lxml')
        currency_block = soup.find('div', class_="converter-container__inputs")

        if currency_block:

            currency_abbr_elements = currency_block.find_all('span', class_="converter-container__item-currency-abbr")
            currency_name_elements = currency_block.find_all('div', class_="converter-container__item-currency-name")

            if currency_name_elements and currency_abbr_elements:
                currency_name_list = []
                currency_type_list = []

                for currency_type in currency_abbr_elements:
                    currency_type_list.append(currency_type.text.strip())

                for currency_name in currency_name_elements:
                    currency_name_list.append(currency_name.text.strip())

                return list(zip(currency_type_list, currency_name_list))

    raise WebElementNotFoundError


def load_currencies_into_enum(currencies_zipper: list) -> None:

    for name, value in currencies_zipper:
        extend_enum(WalletBalanceCurrenciesEnum, name, value)