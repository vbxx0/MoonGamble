import logging

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from pydantic import ValidationError

from src.providers.dependencies import get_current_active_user
from src.providers.pragmatic.schemas import BalanceRequest, BetRequest, WinRequest, RefundRequest, RollbackRequest
from src.providers.schemas import SelfValidateResponse, ReadProfile
from src.providers.pragmatic.utils import make_request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/providers/pragmatic",
                   tags=["Providers", "Pragmatic"])


@router.get("/games")
async def get_games():
    return await make_request("GET", "games")


@router.post("/games/lobby")
async def get_lobby(game_uuid: str, currency: str, ):
    params = {"game_uuid": game_uuid, "currency": currency}
    return await make_request("GET", "games/lobby", params)


@router.post("/games/init")
async def init_game_session(game_uuid: str, player_id: str, player_name: str, currency: str, session_id: str,
                            return_url: str = None, language: str = None,
                            ):
    data = {
        "game_uuid": game_uuid,
        "player_id": player_id,
        "player_name": player_name,
        "currency": currency,
        "session_id": session_id,
        "return_url": return_url,
        "language": language,
    }
    return await make_request("POST", "games/init", data=data)


@router.post("/callback")
async def callback(
        action: str = Query(...),
        player_id: str = Query(None),
        game_uuid: str = Query(None),
        amount: float = Query(None),
        currency: str = Query(None),
        transaction_id: str = Query(None),
        session_id: str = Query(None),
        type: str = Query(None),
        bet_transaction_id: str = Query(None),
        rollback_transactions: str = Query(None),
        freespin_id: str = Query(None),
        quantity: int = Query(None),
        valid_from: int = Query(None),
        valid_until: int = Query(None),
        player_name: str = Query(None),
        denomination: float = Query(None)
):
    try:
        if action == "balance":
            return await handle_balance(BalanceRequest(
                player_id=player_id,
                currency=currency,
                session_id=session_id
            ))
        elif action == "bet":
            return await handle_bet(BetRequest(
                player_id=player_id,
                game_uuid=game_uuid,
                amount=amount,
                currency=currency,
                transaction_id=transaction_id,
                session_id=session_id,
                type=type
            ))
        elif action == "win":
            return await handle_win(WinRequest(
                player_id=player_id,
                game_uuid=game_uuid,
                amount=amount,
                currency=currency,
                transaction_id=transaction_id,
                session_id=session_id,
                type=type
            ))
        elif action == "refund":
            return await handle_refund(RefundRequest(
                player_id=player_id,
                game_uuid=game_uuid,
                amount=amount,
                currency=currency,
                transaction_id=transaction_id,
                session_id=session_id,
                bet_transaction_id=bet_transaction_id
            ))
        elif action == "rollback":
            return await handle_rollback(RollbackRequest(
                player_id=player_id,
                game_uuid=game_uuid,
                currency=currency,
                transaction_id=transaction_id,
                rollback_transactions=rollback_transactions.split(",") if rollback_transactions else []
            ))
        elif action == "freespins/set":
            return await set_freespin_campaign(player_id=player_id,
                                               player_name=player_name,
                                               currency=currency,
                                               quantity=quantity,
                                               valid_from=valid_from,
                                               valid_until=valid_until,
                                               game_uuid=game_uuid,
                                               freespin_id=freespin_id,
                                               bet_id=None,
                                               total_bet_id=None,
                                               denomination=denomination)
        elif action == "freespins/get":
            return await get_freespin_campaign(freespin_id=freespin_id)
        elif action == "freespins/cancel":
            return await cancel_freespin_campaign(freespin_id=freespin_id)
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
    except ValidationError:
        raise HTTPException(status_code=422, detail=f"Incorrect fields for type `{action}`")


async def handle_balance(balance_request: BalanceRequest):
    data = {
        "action": "balance",
        "player_id": balance_request.player_id,
        "currency": balance_request.currency,
        "session_id": balance_request.session_id,
    }
    return await make_request("POST", "balance", data=data)


async def handle_bet(bet_request: BetRequest):
    data = {
        "action": "bet",
        "player_id": bet_request.player_id,
        "game_uuid": bet_request.game_uuid,
        "amount": bet_request.amount,
        "currency": bet_request.currency,
        "transaction_id": bet_request.transaction_id,
        "session_id": bet_request.session_id,
        "type": bet_request.type,
    }
    return await make_request("POST", "bet", data=data)


async def handle_win(win_request: WinRequest):
    data = {
        "action": "win",
        "player_id": win_request.player_id,
        "game_uuid": win_request.game_uuid,
        "amount": win_request.amount,
        "currency": win_request.currency,
        "transaction_id": win_request.transaction_id,
        "session_id": win_request.session_id,
        "type": win_request.type,
    }
    return await make_request("POST", "win", data=data)


async def handle_refund(refund_request: RefundRequest):
    data = {
        "action": "refund",
        "player_id": refund_request.player_id,
        "game_uuid": refund_request.game_uuid,
        "amount": refund_request.amount,
        "currency": refund_request.currency,
        "transaction_id": refund_request.transaction_id,
        "session_id": refund_request.session_id,
        "bet_transaction_id": refund_request.bet_transaction_id,
    }
    return await make_request("POST", "refund", data=data)


async def handle_rollback(rollback_request: RollbackRequest):
    data = {
        "action": "rollback",
        "player_id": rollback_request.player_id,
        "game_uuid": rollback_request.game_uuid,
        "currency": rollback_request.currency,
        "transaction_id": rollback_request.transaction_id,
        "rollback_transactions": rollback_request.rollback_transactions,
    }
    return await make_request("POST", "rollback", data=data)


@router.get("/limits")
async def get_limits():
    return await make_request("GET", "limits")


@router.get("/limits/freespin")
async def get_freespin_limits():
    return await make_request("GET", "limits/freespin")


@router.get("/jackpots")
async def get_jackpots():
    return await make_request("GET", "jackpots")


@router.post("/balance/notify")
async def notify_balance_change(balance: float, session_id: str, ):
    data = {
        "balance": balance,
        "session_id": session_id
    }
    return await make_request("POST", "balance/notify", data=data)


@router.get("/freespins/bets")
async def get_freespin_bets(game_uuid: str, currency: str, ):
    params = {"game_uuid": game_uuid, "currency": currency}
    return await make_request("GET", "freespins/bets", params)


@router.post("/freespins/set")
async def set_freespin_campaign(player_id: str, player_name: str, currency: str, quantity: int, valid_from: int,
                                valid_until: int, game_uuid: str, freespin_id: str, bet_id: int = None,
                                total_bet_id: int = None, denomination: float = None,
                                ):
    data = {
        "player_id": player_id,
        "player_name": player_name,
        "currency": currency,
        "quantity": quantity,
        "valid_from": valid_from,
        "valid_until": valid_until,
        "game_uuid": game_uuid,
        "freespin_id": freespin_id,
        "bet_id": bet_id,
        "total_bet_id": total_bet_id,
        "denomination": denomination
    }
    return await make_request("POST", "freespins/set", data=data)


@router.get("/freespins/get")
async def get_freespin_campaign(freespin_id: str, ):
    params = {"freespin_id": freespin_id}
    return await make_request("GET", "freespins/get", params)


@router.post("/freespins/cancel")
async def cancel_freespin_campaign(freespin_id: str, ):
    data = {"freespin_id": freespin_id}
    return await make_request("POST", "freespins/cancel", data=data)


@router.post("/self-validate", response_model=SelfValidateResponse)
async def self_validate():
    return await make_request("POST", "self-validate")
