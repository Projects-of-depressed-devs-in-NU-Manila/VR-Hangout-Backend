from fastapi import APIRouter, WebSocket, Query, WebSocketDisconnect, HTTPException
from app.services.connection.connection import ConnectionService 

from app.core.vector import Vector3


import traceback

router = APIRouter(prefix="/game", tags=["Game Websocket"])

world_service = ConnectionService()

@router.websocket("/ws")
async def handler(websocket: WebSocket, player_id:str = Query(None)):
    if player_id == None:
        await websocket.close()
        raise HTTPException(501, {"error": "Please Provide a valid player id"})
    
    if player_id in world_service.players.keys():
        await websocket.close()
        raise HTTPException(401, {"error": "Player is playing already"})

    await websocket.accept()
    player = await world_service.connect(player_id=player_id, websocket=websocket)

    while True:
        try:
            data = await websocket.receive_json()

            match data["type"]:
                case "playerMove":
                    player.position =  Vector3(**data["position"])

 
            await world_service.broadcast(player_id, data)
        except WebSocketDisconnect as e:
            break
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            raise HTTPException(500, {"error": "Internal Server Error"})
 
    await world_service.disconnect(player_id)
    print("Current Players: ", len(world_service.players))

    


