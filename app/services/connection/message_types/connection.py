from app.core.player import Player
import json

def create_connection_message(player: Player):
    return {
            "type": "playerConnect", 
            "playerId": player.id,
            "position": player.position.model_dump()
            }

def create_disconection_message(player_id: str):
    return {
            "type": "playerDisconnect", 
            "playerId": player_id
            }
