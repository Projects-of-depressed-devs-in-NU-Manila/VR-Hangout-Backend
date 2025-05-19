from app.core.vector import Vector3

from fastapi import WebSocket


class Player:
    websocket: WebSocket
    id: str
    current_world_id: str
    position: Vector3  = Vector3()
    rotation: Vector3  = Vector3()

    def __init__(self, websocket, id, current_world_id):
        self.websocket = websocket
        self.id = id
        self.current_world_id = current_world_id