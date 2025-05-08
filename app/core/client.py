from app.core.vector import Vector3
from fastapi import WebSocket


class Client:
    websocket: WebSocket
    user_id: str
    current_world_id: str
    position: Vector3  
    rotation: Vector3  