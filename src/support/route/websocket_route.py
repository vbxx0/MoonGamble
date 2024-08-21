import logging
from typing import Annotated, Optional, Union

from fastapi import (APIRouter, Depends, Query, WebSocket, WebSocketDisconnect,
                     WebSocketException)
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.support.models import Message
from src.support.schemas import ReadMessage
from src.users.route import get_current_user

from .websocket_manager import TicketConnectionManager

router = APIRouter()

logger = logging.getLogger('websocket')
logging.basicConfig(level=logging.DEBUG)
manager = TicketConnectionManager()


async def websocket_get_current_user(
    websocket: WebSocket,
    token: Annotated[Union[str, None], Query()] = None
):
    return await get_current_user(token)


@router.websocket('/ws/ticket/{ticket_id}/')
async def websocket_ticket_chat(
    websocket: WebSocket,
    ticket_id: int,
    token: Optional[str] = None,
    # user: ReadProfile = Depends(websocket_get_current_user),
    db: AsyncSession = Depends(get_session)
) -> None:
    """Endpoint for support chat."""
    user = await get_current_user(token)
    user_id = user.id
    await manager.connect(ticket_id, websocket)
    try:
        while True:
            if (data := await websocket.receive_json()):
                logger.info(f'WebSocket Debug // Data {data}')
                # message = SendMessage.model_validate(data)
                db_message = Message(
                    content=data["message"],
                    from_id=user_id,
                    ticket_id=ticket_id
                )
                db.add(db_message)
                await db.commit()
                await db.refresh(db_message)

                new_message = ReadMessage(
                    content=db_message.content,
                    from_id=db_message.from_id,
                    ticket_id=ticket_id,
                    created_at=str(db_message.created_at),
                    updated_at=str(db_message.created_at)
                )

                await manager.broadcast(ticket_id, new_message)
    except (WebSocketDisconnect, WebSocketException) as e:
        logger.error(str(e))
        await manager.disconnect(ticket_id, websocket)
