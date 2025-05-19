from fastapi import APIRouter, WebSocket, Query, WebSocketDisconnect, HTTPException
from app.services.connection.connection import ConnectionService 
from app.services.world.worlds import WorldService, WorldObject, World
from app.database.session import create_postgres_session

from app.core.vector import Vector3


import traceback

router = APIRouter(prefix="/game", tags=["Game Websocket"])

connection_service = ConnectionService()

@router.websocket("/ws")
async def handler(websocket: WebSocket, player_id:str = Query(None)):
    if player_id == None:
        await websocket.close(code=4000)
        return
    
    if player_id in connection_service.players.keys():
        await websocket.close(code=4001, reason="Player already connected")
        return

    await websocket.accept()

    world: World 
    with create_postgres_session() as session:
        world = WorldService.get_world_by_player_id(session, player_id)

    player = await connection_service.add(player_id, websocket, str(world.world_id))
 
    try:
        while True:
                data = await websocket.receive_json()

                match data["type"]:
                    case "playerMove":
                        player.position =  Vector3(**data["position"])

                await connection_service.broadcast(player_id, data)
    except WebSocketDisconnect as e:
        print(f"Player {player_id} disconnected")
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        await websocket.close(code=1011, reason="Internal Server Error")
    finally:
        await connection_service.remove(player_id)
        print("Current Players: ", len(connection_service.players))
        await websocket.close()