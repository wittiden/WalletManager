import pytest


@pytest.mark.unit
class TestUserRepository:
    """Класс для тестирования репозитория для хранения пользователей"""

    def test_add_user_good(self, user_repository, client_sample):
        user_repository.add_user(client_sample)
        user_repository.get_user(client_sample.item_id)

        assert len(user_repository.get_all_users()) == 1