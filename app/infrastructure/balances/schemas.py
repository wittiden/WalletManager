from decimal import Decimal

from pydantic import BaseModel, field_validator, Field

class CreateRegularBalanceSchema(BaseModel):
    """"""

    amount: Decimal = Field(gt=0)
    currency: str


class CreateForeignBalanceSchema(BaseModel):
    """"""

    amounts: list[Decimal] = Field(gt=0)
    currencies: list[str]


class CloseBalanceSchema(BaseModel):
    """"""

