import pytest

from app.common.enums.wallet_enums import WalletTypesEnum
from app.core.utils import get_hash
from app.infrastructure.wallets.schemas import CreateWalletSchema, CloseWalletSchema
from app.infrastructure.wallets.use_cases import WalletServiceFacade
from tests.integration.conftest import load_admin_to_db


class TestWalletServiceFacade:
    """Класс для тестирования работы фасада операций над кошельками"""

    @pytest.mark.integration
    @pytest.mark.parametrize('key, pin', [
        (WalletTypesEnum.DEBIT, '1234'),
        (WalletTypesEnum.CREDIT, '1234'),
    ])
    def test_create_wallet_good(self, container, load_client_to_db, key, pin):
        facade = container.get(WalletServiceFacade)

        user = load_client_to_db
        schema = CreateWalletSchema(key=key, pin=pin)

        wallet = facade.create_wallet(user, schema)

        assert wallet.pin == get_hash(pin)
        assert wallet.owner_id == user.item_id
        assert wallet.account_type == key

    @pytest.mark.integration
    def test_show_wallet_good(self, container, load_client_to_db):
        facade = container.get(WalletServiceFacade)

        user = load_client_to_db
        schema = CreateWalletSchema(key=WalletTypesEnum.DEBIT, pin='1234')
        wallet = facade.create_wallet(user, schema)

        find_wallets = facade.show_my_wallets(user)

        for w in find_wallets:
            assert w.pin == wallet.pin
            assert w.owner_id == wallet.owner_id
            assert w.account_type == wallet.account_type

    @pytest.mark.integration
    def test_block_wallet_good(self, container, load_client_to_db, load_admin_to_db):
        facade = container.get(WalletServiceFacade)

        user = load_client_to_db
        admin = load_admin_to_db
        schema = CreateWalletSchema(key=WalletTypesEnum.DEBIT, pin='1234')
        wallet = facade.create_wallet(user, schema)

        facade.block_wallet(admin, wallet.item_id)

        blocked_wallet = facade.show_wallet(admin, wallet.item_id)
        assert blocked_wallet.pin == wallet.pin
        assert blocked_wallet.owner_id == wallet.owner_id
        assert blocked_wallet.is_blocked is True
        assert blocked_wallet.account_type == wallet.account_type

    @pytest.mark.integration
    def test_unblock_wallet_good(self, container, load_client_to_db, load_admin_to_db):
        facade = container.get(WalletServiceFacade)

        user = load_client_to_db
        admin = load_admin_to_db
        schema = CreateWalletSchema(key=WalletTypesEnum.DEBIT, pin='1234')
        wallet = facade.create_wallet(user, schema)
        facade.block_wallet(admin, wallet.item_id)

        facade.unblock_wallet(admin, wallet.item_id)

        blocked_wallet = facade.show_wallet(admin, wallet.item_id)
        assert blocked_wallet.pin == wallet.pin
        assert blocked_wallet.owner_id == wallet.owner_id
        assert blocked_wallet.is_blocked is False
        assert blocked_wallet.account_type == wallet.account_type

    @pytest.mark.integration
    def test_close_wallet(self, container, load_client_to_db, load_admin_to_db):
        facade = container.get(WalletServiceFacade)

        user = load_client_to_db
        admin = load_admin_to_db
        schema = CreateWalletSchema(key=WalletTypesEnum.DEBIT, pin='1234')
        wallet = facade.create_wallet(user, schema)

        close_schema = CloseWalletSchema(pin=schema.pin, address=wallet.address)
        facade.close_wallet(user, close_schema)

        with pytest.raises(ValueError):
            facade.show_wallet(admin, wallet.item_id)
