from app.models.worlds import World
from app.models.world_objects import WorldObject
from app.core.id_gen import generate_id

from app.database.session import create_postgres_session

from sqlalchemy.orm import Session


class WorldService():

    @staticmethod
    def create_default_world(session: Session, player_id: str):
        world_id = generate_id(World, World.world_id)
        world = World(world_id=world_id, owner_player_id=player_id)
        session.add(world)
        session.flush()

        world_object_id = generate_id(WorldObject, WorldObject.world_object_id)
        object_id = "plane001"
        scale = [4.0, 4.0, 4.0]

        plane = WorldObject(world_object_id=world_object_id, world_id=world_id, object_id=object_id, scale=scale, position=[0.0, 0.0, 0.0], rotation=[0.0, 0.0, 0.0])
        session.add(plane)
        session.flush()

        return world_object_id
    
