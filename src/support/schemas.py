from datetime import datetime

from pydantic import BaseModel, Field

from src.schemas import ORM

from .models import TicketStatus


class ReadDateTime(ORM):
    created_at: datetime | str
    updated_at: datetime | str = None


class SendMessage(ORM):
    content: dict[str, str]


class ReadMessageSender(ORM):
    fullname: str
    role: str


class ReadMessage(ReadDateTime):
    content: str
    from_id: int
    ticket_id: int


class CreateTicket(BaseModel):
    subject: str = Field(max_length=128)
    message: str


class ReadTicket(ReadDateTime):
    id: int
    subject: str
    status: TicketStatus
