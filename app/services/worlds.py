import json

from app.core.client import Client
from app.core.world import World 

from app.config import default_world_id

class MessageFactory:
    @staticmethod
    def create_connection_message(user_id: str):
        return {
                "type": "client_connect", 
                "data": {
                        "user_id": user_id
                    }
                }

    @staticmethod
    def create_disconection_message(user_id: str):
        return {
                "type": "client_disconnect", 
                "data": {
                        "user_id": user_id
                    }
                }


class WorldService:
    worlds: dict[str, World] = {}# key: world_id 
    clients: dict[str, Client] = {}# key: user_id 

    async def connect(self, user_id: str, websocket ):
        client = Client()
        client.user_id = user_id
        client.websocket = websocket
        client.current_world_id = default_world_id
        self.clients[user_id] = client
        print(self.clients)

        self.add_to_world(default_world_id, user_id)

        await self.broadcast(user_id, MessageFactory.create_connection_message(user_id)) 
    
    async def disconnect(self, user_id: str):
        await self.broadcast(user_id, MessageFactory.create_disconection_message(user_id))
        client = self.clients[user_id]
        self.remove_from_world(client.current_world_id, user_id)
        self.clients.pop(user_id)

    def change_world(self, new_world_id: str, user_id: str):
        old_world_id = self.clients[user_id].current_world_id
        self.remove_from_world(old_world_id, user_id)
        self.add_to_world(new_world_id, user_id)
    
    async def broadcast(self, user_id: str, message: dict): # TODO create more functions for this but with different message types if needed
        world_id = self.clients[user_id].current_world_id

        for id in self.worlds[world_id].cliend_ids :
            if id == user_id:
                continue
            
            client = self.clients[id]
            await client.websocket.send_json(message)
  
    def add_to_world(self, world_id: str, user_id: str):
        if world_id not in self.worlds.keys():
            self.worlds[world_id] = World(world_id, [user_id, ])
        else:
            self.worlds[world_id].cliend_ids.add(user_id)

    def remove_from_world(self, world_id: str, user_id: str):
        self.worlds[world_id].cliend_ids.remove(user_id)

