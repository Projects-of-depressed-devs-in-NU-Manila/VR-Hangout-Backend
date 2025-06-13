from app.core.vector import Vector3

from fastapi import WebSocket


class Player:
    websocket: WebSocket
    voice_websocket: WebSocket | None
    id: str
    current_world_id: str
    position: Vector3  = Vector3()
    rotation: Vector3  = Vector3()
    avatar_name: str = "Bartender"

    def __init__(self, websocket, id, current_world_id, avatar_name):
        self.websocket = websocket
        self.voice_websocket = None
        self.id = id
        self.current_world_id = current_world_id
        self.avatar_name = avatar_name