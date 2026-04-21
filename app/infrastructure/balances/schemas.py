from decimal import Decimal

from pydantic import BaseModel, Field
from app.common.enums.balance_enums import BalanceTypesEnum


class CreateRegularBalanceSchema(BaseModel):
    """Класс схема для проверки полей при создании regular баланса"""

    key: 'BalanceTypesEnum'
    amount: Decimal = Field(gt=0)
    currency: str


class CreateForeignBalanceSchema(BaseModel):
    """Класс схема для проверки полей при создании foreign баланса"""

    key: 'BalanceTypesEnum'
    amounts: list[Decimal]
    currencies: list[str]

