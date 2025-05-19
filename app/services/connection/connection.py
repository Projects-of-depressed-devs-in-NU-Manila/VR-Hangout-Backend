from fastapi import WebSocket
import time

from app.config import default_world_id
from app.services.connection.player import Player
from app.services.connection.world import World 
from app.services.connection.message_types.connection import create_connection_message, create_disconection_message
from app.services.connection.message_types.world import create_load_world_message

from app.services.world.worlds import WorldService, WorldObject
from app.database.session import create_postgres_session


# Handles connection and separation between worlds
class ConnectionService:
    worlds: dict[str, World] = {}# key: world_id 
    players: dict[str, Player] = {}# key: player_id 

    async def add(self, player_id: str, websocket: WebSocket, world_id: str = default_world_id):
        player = Player(websocket, player_id, world_id)
        self.players[player_id] = player

        if world_id in self.worlds.keys():
            for id in self.worlds[world_id].player_ids:
                await websocket.send_json(create_connection_message(self.players[id]))

        await self.load_world(player_id, world_id)
        self.add_to_world(world_id, player_id)

        await self.broadcast(player_id, create_connection_message(self.players[player_id])) 
        print(f"Player {player_id} connected to world: {world_id}\n{world_id} Total Players: {len(self.worlds[world_id].player_ids)}")

        return player
     
    async def remove(self, player_id: str):
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

    async def load_world(self, player_id, world_id):
        world_objects: list[WorldObject] = []
        with create_postgres_session() as session:
            world_objects = WorldService.get_world_objects_by_world_id(session, world_id)
    
        await self.players[player_id].websocket.send_json(create_load_world_message(world_objects))
        
 

