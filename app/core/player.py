from app.core.vector import Vector3
from fastapi import WebSocket


class Player:
    websocket: WebSocket
    id: str
    current_world_id: str
    position: Vector3  = Vector3()
    rotation: Vector3  = Vector3()