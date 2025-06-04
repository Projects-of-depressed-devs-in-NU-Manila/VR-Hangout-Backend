from fastapi import APIRouter, WebSocket, Query, WebSocketDisconnect, HTTPException
from app.services.connection.connection import ConnectionService 
from app.services.world.worlds import WorldService, WorldObject, World
from app.database.session import create_postgres_session
from app.services.connection.message_types.world_data import WorldData 

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
    world_objects: list[WorldObject] = []
    with create_postgres_session() as session:
        world = WorldService.get_world_by_player_id(session, player_id)
        world_objects = WorldService.get_world_objects_by_world_id(session, str(world.world_id))

    data = WorldData(type="loadWorldObjects", world_id=str(world.world_id), objects=world_objects)
    await websocket.send_json(data.to_json())

    player = await connection_service.add(player_id, websocket, str(world.world_id))
  
    try:
        while True:
                data = await websocket.receive_json()

                match data["type"]:
                    case "playerMove":
                        player.position =  Vector3(**data["position"])
                    case "addWorldObjects":
                        print("Adding world objects")
                        with create_postgres_session() as session:
                            WorldService.add_world_objects(session, WorldData.from_json(data))
                            session.commit()
                    case "editWorldObjects":
                        with create_postgres_session() as session:
                            WorldService.edit_world_objects(session, WorldData.from_json(data))
                            session.commit()
                    case "changeWorld":
                        await connection_service.change_world(data["worldId"], player_id)
                        continue
                        

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

@router.websocket("/voice")
async def voice_handler(websocket: WebSocket, player_id: str = Query(None)):
    if player_id not in connection_service.players.keys():
        await websocket.close(code=4001, reason="Player Not yet connected to game server")
        return
    
    if connection_service.players[player_id].voice_websocket != None:
        await websocket.close(code=4001, reason="Player voice is already connected")
        return
    await websocket.accept()

    connection_service.players[player_id].voice_websocket = websocket
     
    try: 
        while True:
            data = await websocket.receive_json()

            await connection_service.broadcast_voice(player_id, data)
    except WebSocketDisconnect as e:
        print(f"Player {player_id} disconnected")
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        await websocket.close(code=1011, reason="Internal Server Error")
    finally:
        await websocket.close()