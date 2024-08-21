from typing import Mapping

from fastapi import WebSocket

from ..schemas import ReadMessage


class TicketConnectionManager:
    """Websocket implementation for support chat."""
    def __init__(self) -> None:
        self.active_connections: Mapping[int, list[WebSocket]] = {}

    def get_connection(self, ticket_id: int) -> list[WebSocket]:
        if ticket_id not in self.active_connections:
            self.active_connections[ticket_id] = []
        return self.active_connections[ticket_id]

    async def connect(self, ticket_id: int, websocket: WebSocket):
        await websocket.accept()
        connection = self.get_connection(ticket_id)
        connection.append(websocket)

    async def broadcast(self, ticket_id: int, message: ReadMessage):
        connection = self.get_connection(ticket_id)
        for websocket in connection:
            await websocket.send_json(message.model_dump())

    async def disconnect(self, ticket_id: int, websocket: WebSocket):
        connection = self.get_connection(ticket_id)
        await connection.remove(websocket)
