from app.services.connection.player import Player
import json

def create_connection_message(player: Player):
    return {
            "type": "playerConnect", 
            "playerId": player.id,
            "position": player.position.model_dump(),
            "avatar_name": player.avatar_name
            }

def create_disconection_message(player_id: str):
    return {
            "type": "playerDisconnect", 
            "playerId": player_id
            }
