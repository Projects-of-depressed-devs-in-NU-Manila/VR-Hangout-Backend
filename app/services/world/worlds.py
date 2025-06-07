from app.models.worlds import World
from app.models.world_objects import WorldObject
from app.core.id_gen import generate_id
from app.services.connection.message_types.world_data import WorldData
from sqlalchemy import Column


from sqlalchemy.orm import Session


class WorldService():

    @staticmethod
    def create_default_world(session: Session, player_id: str) -> str:
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
    
    @staticmethod
    def load_player_world(session: Session, player_id: str):
        world = WorldService.get_world_by_player_id(session, player_id)
        world_objects = WorldService.get_world_objects_by_world_id(session, world_id=str(world.world_id))
        data = WorldData(type="loadWorldObjects", world_id=str(world.world_id), objects=world_objects)
        return data
    
    @staticmethod
    def load_world(session: Session, world_id: str):
        world = session.query(World).filter(World.world_id == world_id).one()
        world_objects = WorldService.get_world_objects_by_world_id(session, world_id=str(world.world_id))
        data = WorldData(type="loadWorldObjects", world_id=str(world.world_id), objects=world_objects)
        return data
    
    @staticmethod
    def add_world_objects(session: Session, world_data: WorldData):
        for world_object in world_data.objects:
            id = generate_id(WorldObject, WorldObject.world_object_id)
            world_object.world_object_id = id #type: ignore
            world_object.world_id = world_object.world_id
            session.add(world_object)
            print(world_object.to_json())
            print(f"Adding object {world_object.object_id}")
     
    @staticmethod
    def edit_world_objects(session: Session, world_data: WorldData):
        for world_object in world_data.objects:
            world_object_ = session.query(WorldObject).filter(WorldObject.world_object_id == world_object.world_object_id).one()

            if world_object_ is None:
                raise Exception("Cannot edit world object that does not exist")
        
            world_object_.position = world_object.position
            world_object_.rotation = world_object.rotation
            world_object_.scale = world_object_.scale
        
            session.add(world_object_)
            
    @staticmethod
    def get_world_by_player_id(session: Session, player_id: str) -> World:
        return session.query(World).filter(World.owner_player_id == player_id).one()
    
    @staticmethod
    def get_world_objects_by_world_id(session: Session, world_id: str) -> list[WorldObject]:
        return session.query(WorldObject).filter(WorldObject.world_id == world_id).all()
    
