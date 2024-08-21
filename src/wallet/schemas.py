from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field

from src.schemas import ORM

from .models import PaymentSystem, TransactionType, TransactionStatus

_amount = Field(gt=0.0)


class CreateDeposit(ORM):
    payment_system: PaymentSystem
    amount: Decimal = _amount


class CreateWithdrawal(ORM):
    payment_system: PaymentSystem
    amount: Decimal = _amount


class CreateTransaction(ORM):
    payment_system: PaymentSystem
    type: TransactionType
    from_account: str = ''
    to_account: str = ''
    amount: Decimal
    user_id: int
    status: TransactionStatus = TransactionStatus.CONFIRMED


class ReadTransaction(ORM):
    id: int
    payment_system: PaymentSystem
    type: TransactionType
    amount: Decimal
    from_account: str
    to_account: str
    created_at: datetime
    status: TransactionStatus
    user_id: int


class ReadTransactionsPaginated(ORM):
    total: int
    transactions: List[ReadTransaction]


class ReadBalance(BaseModel):
    balance: Decimal
    bonus_balance: Decimal
    pure_balance: Decimal


class ReadBonusEarned(BaseModel):
    amount: Decimal
    balance: Decimal
