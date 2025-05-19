from fastapi import APIRouter, WebSocket, Query, WebSocketDisconnect, HTTPException
from app.services.connection.connection import ConnectionService 
from app.services.world.worlds import WorldService, WorldObject, World
from app.database.session import create_postgres_session

from app.core.vector import Vector3


import traceback

router = APIRouter(prefix="/chat", tags=["Game Websocket"])

connection_service = ConnectionService()

@router.websocket("/ws")
async def handler(websocket: WebSocket, player_id:str = Query(None), world_id:str = Query(None)):
    if player_id == None:
        await websocket.close(code=4000)
        return
    
    if player_id in connection_service.players.keys():
        await websocket.close(code=4001, reason="Player already connected")
        return

    await websocket.accept()

    player = await connection_service.add(player_id, websocket, str(world_id))
 
    try:
        while True:
                data : dict = await websocket.receive_json()

                await connection_service.broadcast(player_id, data)
    except WebSocketDisconnect as e:
        print(f"Player {player_id} disconnected")
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        await websocket.close(code=1011, reason="Internal Server Error")
    finally:
        await connection_service.remove(player_id)
        await websocket.close()
        print("Current Players: ", len(connection_service.players))