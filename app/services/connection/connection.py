from fastapi import WebSocket
import time

from app.config import default_world_id
from app.core.vector import Vector3
from app.services.connection.player import Player
from app.services.connection.world import World 
from app.services.connection.message_types.connection import create_connection_message, create_disconection_message

from app.services.world.worlds import WorldService, WorldObject
from app.database.session import create_postgres_session


# Handles connection and separation between worlds
class ConnectionService:
    worlds: dict[str, World] = {}# key: world_id 
    players: dict[str, Player] = {}# key: player_id 

    async def add(self, player_id: str, websocket: WebSocket, world_id: str = default_world_id, avatar_name: str = "Bartender"):
        player = Player(websocket, player_id, world_id, avatar_name)
        self.players[player_id] = player

        if world_id in self.worlds.keys():
            for id in self.worlds[world_id].player_ids:
                await websocket.send_json(create_connection_message(self.players[id]))

        self.add_to_world(world_id, player_id)

        await self.broadcast(player_id, create_connection_message(self.players[player_id])) 
        print(f"Player {player_id} connected to world: {world_id}\n{world_id} Total Players: {len(self.worlds[world_id].player_ids)}")

        return player
     
    async def remove(self, player_id: str):
        await self.broadcast(player_id, create_disconection_message(player_id))
        player = self.players[player_id]
        self.remove_from_world(player.current_world_id, player_id)
        self.players.pop(player_id)

    async def go_to_hub(self, player_id: str):
        player = self.players[player_id]

        old_world_id = self.players[player_id].current_world_id
        if "hub" == old_world_id:
            return

        self.players[player_id].current_world_id = "hub" 
        self.players[player_id].position = Vector3() 
        self.players[player_id].rotation = Vector3() 
        self.remove_from_world(old_world_id, player_id)
        self.add_to_world("hub", player_id)

        if player.current_world_id in self.worlds.keys():
            for id in self.worlds[player.current_world_id].player_ids:
                await player.websocket.send_json(create_connection_message(self.players[id])) if id != player_id else ...

        await self.broadcast(player_id, create_connection_message(self.players[player_id])) 

    async def change_world(self, new_world_id: str, player_id: str):
        #TODO: send the player the world data use this when loading the world for the first time
        try:
            player = self.players[player_id]
            
            old_world_id = self.players[player_id].current_world_id
            if new_world_id == old_world_id:
                return

            self.players[player_id].current_world_id = new_world_id
            self.players[player_id].position = Vector3() 
            self.players[player_id].rotation = Vector3() 
            self.remove_from_world(old_world_id, player_id)
            self.add_to_world(new_world_id, player_id)

            with create_postgres_session() as session:
                data = WorldService.load_world(session, player.current_world_id)
                await player.websocket.send_json(data.to_json())

            if player.current_world_id in self.worlds.keys():
                for id in self.worlds[player.current_world_id].player_ids:
                    await player.websocket.send_json(create_connection_message(self.players[id])) if id != player_id else ...

            await self.broadcast(player_id, create_connection_message(self.players[player_id])) 
        except Exception as e:
            print(e)
    
    async def broadcast(self, player_id: str, message: dict): # TODO create more functions for this but with different message types if needed
        world_id = self.players[player_id].current_world_id

        for id in self.worlds[world_id].player_ids :
            if id == player_id:
                continue
            
            player = self.players[id]
            await player.websocket.send_json(message)
    
    async def broadcast_voice(self, player_id: str, packet: dict):
        player = self.players[player_id]
        for id in self.worlds[player.current_world_id].player_ids:
            if id == player_id:
                continue
 
            other_player = self.players[id]
            if other_player.voice_websocket is None:
                continue

            distance = get_distance(player.position, other_player.position)
            if distance < 8:
                await other_player.voice_websocket.send_json(packet)
  
    def add_to_world(self, world_id: str, player_id: str):
        if world_id not in self.worlds.keys():
            self.worlds[world_id] = World(world_id, [player_id, ])
        else:
            self.worlds[world_id].player_ids.add(player_id)

    def remove_from_world(self, world_id: str, player_id: str):
        self.worlds[world_id].player_ids.remove(player_id)

def get_distance(vec1: Vector3, vec2: Vector3):
    import numpy as np

    a = np.array([vec1.x, vec1.y, vec1.z])
    b = np.array([vec2.x, vec2.y, vec2.z])

    distance = np.linalg.norm(a - b)
    return distance


