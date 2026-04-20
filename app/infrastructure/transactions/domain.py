from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.common.enums.transaction_enums import TransactionStatusesEnum, TransactionTypesEnum
from app.common.mixins import MixinId
from app.core.invariants import DomainInvariant


@dataclass
class TransactionBase(MixinId):
    """Датакласс для хранения данных о базовой транзакции"""

    _from_address: str
    _to_address: str
    _completed_at: datetime
    _amount: Decimal
    _fee: Decimal
    _operation_status: 'TransactionStatusesEnum' = field(default=None, init=False)
    _operation_type: 'TransactionTypesEnum' = field(default=TransactionTypesEnum.UNKNOWN, init=False)

    def __post_init__(self) -> None:
        super().__init__()

        DomainInvariant.no_empty('from_address', self._from_address)
        DomainInvariant.no_empty('to_address', self._to_address)
        DomainInvariant.is_instance('completed_at', self._completed_at, datetime)
        DomainInvariant.no_negative('amount', self._amount)
        DomainInvariant.no_negative('fee', self._fee)

    @property
    def from_address(self) -> str:
        return self._from_address

    @property
    def to_address(self) -> str:
        return self._to_address

    @property
    def completed_at(self) -> datetime:
        return self._completed_at

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def fee(self) -> Decimal:
        return self._fee

    @property
    def operation_status(self) -> 'TransactionStatusesEnum':
        return self._operation_status

    @property
    def operation_type(self) -> 'TransactionTypesEnum':
        return self._operation_type

    @from_address.setter
    def from_address(self, value: str) -> None:
        self._from_address = DomainInvariant.no_empty('from_address', value)

    @to_address.setter
    def to_address(self, value: str) -> None:
        self._to_address = DomainInvariant.no_empty('to_address', value)

    @completed_at.setter
    def completed_at(self, value: datetime) -> None:
        self._completed_at = DomainInvariant.is_instance('completed_at', value, datetime)

    @amount.setter
    def amount(self, value: Decimal) -> None:
        self._amount = DomainInvariant.no_negative('amount', value)

    @fee.setter
    def fee(self, value: Decimal) -> None:
        self._fee = DomainInvariant.no_negative('fee', value)

    @operation_status.setter
    def operation_status(self, value: 'TransactionStatusesEnum') -> None:
        self._operation_status = value

    def __repr__(self) -> str:
        return f'#{self.item_id} -> {self._operation_type.value}\nStatus: {self._operation_status.value}, from_address: {self._from_address}, to_address: {self._to_address}, amount: {self._amount}, fee: {self._fee}, completed_at: {self._completed_at}'

    __str__ = __repr__


@dataclass
class DepositTransaction(TransactionBase):
    """Датакласс для хранения данных о транзакции пополнения"""

    _deposit_currency: str

    def __post_init__(self) -> None:
        super().__post_init__()

        self._operation_type = TransactionTypesEnum.DEPOSIT

        DomainInvariant.no_empty('deposit_currency', self._deposit_currency)

    @property
    def deposit_currency(self) -> str:
        return self._deposit_currency

    @deposit_currency.setter
    def deposit_currency(self, value: str) -> None:
        self._deposit_currency = DomainInvariant.no_empty('deposit_currency', value)

    def __repr__(self) -> str:
        return f'{super().__repr__()}, currency: {self._deposit_currency}'

    __str__ = __repr__


@dataclass
class WithdrawTransaction(TransactionBase):
    """Датакласс для хранения данных о транзакции снятия"""

    _withdraw_currency: str

    def __post_init__(self) -> None:
        super().__post_init__()

        self._operation_type = TransactionTypesEnum.WITHDRAW

        DomainInvariant.no_empty('withdraw_currency', self._withdraw_currency)

    @property
    def withdraw_currency(self) -> str:
        return self._withdraw_currency

    @withdraw_currency.setter
    def withdraw_currency(self, value: str) -> None:
        self._withdraw_currency = DomainInvariant.no_empty('withdraw_currency', value)

    def __repr__(self) -> str:
        return f'{super().__repr__()}, currency: {self._withdraw_currency}'

    __str__ = __repr__


@dataclass
class ExchangeTransaction(TransactionBase):
    """Датакласс для хранения данных о транзакции обмена"""

    _from_currency: str
    _to_currency: str

    def __post_init__(self) -> None:
        super().__post_init__()

        self._operation_type = TransactionTypesEnum.EXCHANGE

        DomainInvariant.no_empty('from_currency', self._from_currency)
        DomainInvariant.no_empty('to_currency', self._to_currency)

    @property
    def from_currency(self) -> str:
        return self._from_currency

    @property
    def to_currency(self) -> str:
        return self._to_currency

    @from_currency.setter
    def from_currency(self, value: str) -> None:
        self._from_currency = DomainInvariant.no_empty('from_currency', value)

    @to_currency.setter
    def to_currency(self, value: str) -> None:
        self._to_currency = DomainInvariant.no_empty('to_currency', value)

    def __repr__(self) -> str:
        return f'{super().__repr__()}, from_currency: {self._from_currency}, to_currency: {self._to_currency}'

    __str__ = __repr__
