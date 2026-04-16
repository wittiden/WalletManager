from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from blinker import Signal

from app.common.enums.transaction_enums import TransactionStatusesEnum, TransactionTypesEnum
from app.common.mixins import MixinId
from app.core.utils import blink_func

transaction_update_signal = Signal()
transaction_update_signal.connect(blink_func)


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
        old_value = self._from_address
        self._from_address = value
        transaction_update_signal.send(self, field='from_address', old=old_value, new=value)

    @to_address.setter
    def to_address(self, value: str) -> None:
        old_value = self._to_address
        self._to_address = value
        transaction_update_signal.send(self, field='to_address', old=old_value, new=value)

    @completed_at.setter
    def completed_at(self, value: datetime) -> None:
        old_value = self._completed_at
        self._completed_at = value
        transaction_update_signal.send(self, field='completed_at', old=old_value, new=value)

    @amount.setter
    def amount(self, value: Decimal) -> None:
        old_value = self._amount
        self._amount = value
        transaction_update_signal.send(self, field='amount', old=old_value, new=value)

    @operation_status.setter
    def operation_status(self, value: 'TransactionStatusesEnum') -> None:
        old_value = self._operation_status
        self._operation_status = value
        transaction_update_signal.send(self, field='operation_status', old=old_value, new=value)

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

    @property
    def withdraw_fee(self) -> Decimal:
        return self._withdraw_fee

    @withdraw_fee.setter
    def withdraw_fee(self, value: Decimal) -> None:
        old_value = self._withdraw_fee
        self._withdraw_fee = value
        transaction_update_signal.send(self, field='withdraw_fee', old=old_value, new=value)

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
        old_value = self._exchange_fee
        self._exchange_fee = value
        transaction_update_signal.send(self, field='exchange_fee', old=old_value, new=value)

    @from_currency.setter
    def from_currency(self, value: str) -> None:
        old_value = self._from_currency
        self._from_currency = value
        transaction_update_signal.send(self, field='from_currency', old=old_value, new=value)

    @to_currency.setter
    def to_currency(self, value: str) -> None:
        old_value = self._to_currency
        self._to_currency = value
        transaction_update_signal.send(self, field='to_currency', old=old_value, new=value)

    def __repr__(self) -> str:
        return f'{super().__repr__()}, fee: {self._exchange_fee}, from_currency: {self._from_currency}, to_currency: {self._to_currency}'

    __str__ = __repr__
