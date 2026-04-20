import pytest

from app.common.enums.wallet_enums import WalletTypesEnum
from app.infrastructure.wallets.factory import WalletFactory


class TestWalletFactory:
    """Класс для тестирования фабрики кошельков"""

    @pytest.mark.integration
    @pytest.mark.parametrize('key', [
        WalletTypesEnum.DEBIT,
        WalletTypesEnum.CREDIT,
    ])
    def test_create_wallet_factory(self, container, sample_wallet_base, key):
        wallet_factory = container.get(WalletFactory)

        wallet = wallet_factory.create_wallet(key, sample_wallet_base.pin, sample_wallet_base.owner_id)

        assert wallet.pin == sample_wallet_base.pin
        assert wallet.owner_id == sample_wallet_base.owner_id

