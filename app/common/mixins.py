import uuid


class MixinId:
    """Миксин-класс для создания id"""

    def __init__(self) -> None:
        self._item_id: str = uuid.uuid4().hex[:6]

    @property
    def item_id(self) -> str:
        return self._item_id