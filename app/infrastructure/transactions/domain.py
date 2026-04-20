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
    _operation_status: 'TransactionStatusesEnum'
    _operation_type: 'TransactionTypesEnum' = field(default=TransactionTypesEnum.UNKNOWN, init=False)

    def __post_init__(self) -> None:
        super().__init__()

        DomainInvariant.no_empty('from_address', self._from_address)
        DomainInvariant.no_empty('to_address', self._to_address)
        DomainInvariant.is_instance('completed_at', self._completed_at, datetime)
        DomainInvariant.no_negative('amount', self._amount)
        DomainInvariant.is_instance('operation_status', self._operation_status, TransactionStatusesEnum)

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

    @operation_status.setter
    def operation_status(self, value: 'TransactionStatusesEnum') -> None:
        self._operation_status = DomainInvariant.is_instance('operation_status', value, TransactionStatusesEnum)

    def __repr__(self) -> str:
        return f'#{self.item_id} -> {self._operation_type.value}\nStatus: {self._operation_status.value}, from_address: {self._from_address}, to_address: {self._to_address}, amount: {self._amount}, completed_at: {self._completed_at}'

    __str__ = __repr__


@dataclass
class DepositTransaction(TransactionBase):
    """Датакласс для хранения данных о транзакции пополнения"""

    def __post_init__(self) -> None:
        super().__post_init__()

        self._operation_type = TransactionTypesEnum.DEPOSIT

    def __repr__(self) -> str:
        return f'{super().__repr__()}'

    __str__ = __repr__


@dataclass
class WithdrawTransaction(TransactionBase):
    """Датакласс для хранения данных о транзакции снятия"""

    _withdraw_fee: Decimal

    def __post_init__(self) -> None:
        super().__post_init__()

        self._operation_type = TransactionTypesEnum.WITHDRAW

        DomainInvariant.no_negative('withdraw_fee', self._withdraw_fee)

    @property
    def withdraw_fee(self) -> Decimal:
        return self._withdraw_fee

    @withdraw_fee.setter
    def withdraw_fee(self, value: Decimal) -> None:
        self._withdraw_fee = DomainInvariant.no_negative('withdraw_fee', value)

    def __repr__(self) -> str:
        return f'{super().__repr__()}, fee: {self._withdraw_fee}'

    __str__ = __repr__


@dataclass
class ExchangeTransaction(TransactionBase):
    """Датакласс для хранения данных о транзакции обмена"""

    _exchange_fee: Decimal
    _from_currency: str
    _to_currency: str

    def __post_init__(self) -> None:
        super().__post_init__()

        self._operation_type = TransactionTypesEnum.EXCHANGE

        DomainInvariant.no_negative('exchange_fee', self._exchange_fee)
        DomainInvariant.no_empty('from_currency', self._from_currency)
        DomainInvariant.no_empty('to_currency', self._to_currency)

    @property
    def exchange_fee(self) -> Decimal:
        return self._exchange_fee

    @property
    def from_currency(self) -> str:
        return self._from_currency

    @property
    def to_currency(self) -> str:
        return self._to_currency

    @exchange_fee.setter
    def exchange_fee(self, value: Decimal) -> None:
        self._exchange_fee = DomainInvariant.no_negative('exchange_fee', value)

    @from_currency.setter
    def from_currency(self, value: str) -> None:
        self._from_currency = DomainInvariant.no_empty('from_currency', value)

    @to_currency.setter
    def to_currency(self, value: str) -> None:
        self._to_currency = DomainInvariant.no_empty('to_currency', value)

    def __repr__(self) -> str:
        return f'{super().__repr__()}, fee: {self._exchange_fee}, from_currency: {self._from_currency}, to_currency: {self._to_currency}'

    __str__ = __repr__
