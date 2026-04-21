import pytest
from pytest_mock import MockerFixture

from app.common.enums.wallet_enums import WalletTypesEnum
from app.infrastructure.wallets.domain import CreditWallet, DebitWallet, WalletBase


class TestWalletDomain:
    """Класс для тестирования домена кошельков"""

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'class_type, pin, owner_id, is_blocked, account_type',
        [
            (WalletBase, '1234', 'test123343', False, WalletTypesEnum.UNKNOWN),
            (CreditWallet, '1234', 'test123343', False, WalletTypesEnum.CREDIT),
            (DebitWallet, '1234', 'test123343', False, WalletTypesEnum.DEBIT),
        ],
    )
    def test_wallet_domain_good(self, class_type, pin, owner_id, is_blocked, account_type):
        obj = class_type(pin, owner_id)
        assert obj.pin == pin
        assert obj.owner_id == owner_id
        assert obj.is_blocked == is_blocked
        assert obj.account_type == account_type

    @pytest.mark.unit
    @pytest.mark.parametrize(
        'pin, owner_id',
        [
            ('', 'test13243'),
            ('1234', ''),
        ],
    )
    def test_wallet_domain_bad(self, pin, owner_id):
        with pytest.raises(ValueError):
            WalletBase(pin, owner_id)

    @pytest.mark.unit
    def test_wallet_setters(self, mocker: MockerFixture, sample_wallet_base):
        mock = mocker.patch('app.infrastructure.wallets.domain.wallet_upgrade_signal.send')

        sample_wallet_base.owner_id = 'new_owner_id'

        assert mock.call_count == 1
