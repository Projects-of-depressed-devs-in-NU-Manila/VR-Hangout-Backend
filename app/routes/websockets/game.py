from fastapi import APIRouter, WebSocket, Query, WebSocketDisconnect, HTTPException
from app.services.worlds import WorldService 

import json

import traceback

router = APIRouter(prefix="/game", tags="Game Websocket")

world_service = WorldService()

@router.websocket("/ws")
async def handler(websocket: WebSocket, user_id:str = Query(None)):
    await websocket.accept()
    await world_service.connect(user_id=user_id, websocket=websocket)

    while True:
        try:
            data = await websocket.receive_json()

            await world_service.broadcast(user_id, data)
        except WebSocketDisconnect as e:
            await world_service.disconnect(user_id)
            break
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            raise HTTPException(500, {"error": "Internal Server Error"})


