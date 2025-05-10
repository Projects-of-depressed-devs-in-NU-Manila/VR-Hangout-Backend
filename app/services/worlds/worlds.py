from fastapi import WebSocket
import time

from app.config import default_world_id
from app.core.player import Player
from app.core.world import World 
from app.services.worlds.message_types.connection import create_connection_message, create_disconection_message


class WorldService:
    worlds: dict[str, World] = {}# key: world_id 
    players: dict[str, Player] = {}# key: player_id 

    async def connect(self, player_id: str, websocket: WebSocket ):

        if default_world_id in self.worlds.keys():
            for id in self.worlds[default_world_id].player_ids:
                await websocket.send_json(create_connection_message(self.players[id]))

        player = Player()
        player.id = player_id
        player.websocket = websocket
        player.current_world_id = default_world_id
        self.players[player_id] = player
        print(self.players)

        self.add_to_world(default_world_id, player_id)
 
        await self.broadcast(player_id, create_connection_message(self.players[player_id])) 

        return player
     
    async def disconnect(self, player_id: str):
        await self.broadcast(player_id, create_disconection_message(player_id))
        player = self.players[player_id]
        self.remove_from_world(player.current_world_id, player_id)
        self.players.pop(player_id)

    def change_world(self, new_world_id: str, player_id: str):
        old_world_id = self.players[player_id].current_world_id
        self.remove_from_world(old_world_id, player_id)
        self.add_to_world(new_world_id, player_id)
    
    async def broadcast(self, player_id: str, message: dict): # TODO create more functions for this but with different message types if needed
        world_id = self.players[player_id].current_world_id

        for id in self.worlds[world_id].player_ids :
            if id == player_id:
                continue
            
            player = self.players[id]
            await player.websocket.send_json(message)
  
    def add_to_world(self, world_id: str, player_id: str):
        if world_id not in self.worlds.keys():
            self.worlds[world_id] = World(world_id, [player_id, ])
        else:
            self.worlds[world_id].player_ids.add(player_id)

    def remove_from_world(self, world_id: str, player_id: str):
        self.worlds[world_id].player_ids.remove(player_id)

