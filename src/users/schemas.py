from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import AnyUrl, BaseModel

from src.schemas import ORM

from .models import UserRole


class RegisterUser(BaseModel):
    username: str
    password: str
    fingerprint: str
    fingerprint_hash: Optional[str] = None
    vk_id: Optional[int] = None
    referrer_id: Optional[int] = None
    avatar: Optional[str] = "1"
    role: str = UserRole.user


class ReadProfile(ORM):
    id: int
    username: str
    fullname: Optional[str]
    avatar: Optional[str]
    telegram_id: Optional[int]
    telegram_fullname: Optional[str]
    telegram_username: Optional[str]
    vk_id: Optional[int]
    role: UserRole
    telegram_code: str
    created_at: datetime


class ReadFullUser(ReadProfile):
    active: bool
    password: str


class ReferralsStatistics(ORM):
    last_month: dict
    total_referrals: int
    total_revenue: Decimal
