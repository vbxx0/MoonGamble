from pydantic import BaseModel


class BalanceRequest(BaseModel):
    player_id: str
    currency: str
    session_id: str = None


class BetRequest(BaseModel):
    player_id: str
    game_uuid: str
    amount: float
    currency: str
    transaction_id: str
    session_id: str
    type: str = "bet"


class WinRequest(BaseModel):
    player_id: str
    game_uuid: str
    amount: float
    currency: str
    transaction_id: str
    session_id: str
    type: str = "win"


class RefundRequest(BaseModel):
    player_id: str
    game_uuid: str
    amount: float
    currency: str
    transaction_id: str
    session_id: str
    bet_transaction_id: str


class RollbackRequest(BaseModel):
    player_id: str
    game_uuid: str
    currency: str
    transaction_id: str
    rollback_transactions: list
