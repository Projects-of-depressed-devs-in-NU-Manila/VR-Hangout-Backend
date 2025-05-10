from app.redis_client.models.world import World
from app.redis_client.models.world_object import WorldObject 
from app.redis_client.models.redis_vector import Vector3 
from app.core.id_gen import generate_id


class WorldService():
    @staticmethod

    def create_default_world(player_id: str):
        # position = Vector3(x=0.0, y=0.0, z=0.0)
        # rotation = Vector3(x=0.0, y=0.0, z=0.0)
        # scale = Vector3(x=4.0, y=4.0, z=4.0)

        id = generate_id()
        # obj = WorldObject(object_id="plane001", position=position, rotation=rotation, scale=scale)
        world = World(world_id=id, owner_player_id=player_id, objects=[])

        world.save()

        return id
