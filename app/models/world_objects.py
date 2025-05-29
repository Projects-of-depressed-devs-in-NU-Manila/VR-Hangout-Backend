from sqlalchemy import Column, String, ARRAY, Float, CheckConstraint
from app.database.session import Base, engine


class WorldObject(Base):
    __tablename__= "world_objects"

    world_object_id = Column(String(10), primary_key=True, nullable=False, unique=True)
    world_id = Column(String(10), primary_key=True, index=True, nullable=False)
    object_id = Column(String(50), nullable=False) # Unity prefab id

    position = Column(ARRAY(Float, dimensions=1), default=[0.0, 0.0, 0.0])
    rotation = Column(ARRAY(Float, dimensions=1), default=[0.0, 0.0, 0.0])
    scale = Column(ARRAY(Float, dimensions=1), default=[0.0, 0.0, 0.0])
 
    __table_args__ = (
        CheckConstraint('array_length(position, 1) = 3', name='check_position_3d'),
        CheckConstraint('array_length(rotation, 1) = 3', name='check_rotation_3d'),
        CheckConstraint('array_length(scale, 1) = 3', name='check_scale_3d'),
    )

    @staticmethod
    def from_json(json: dict):
        world_object = WorldObject()
        world_object.world_object_id = json["worldObjectId"]
        world_object.world_id = json["worldId"]
        world_object.object_id = json["objectId"]

        position = json["position"]
        rotation = json["rotation"]
        scale = json["scale"]
        world_object.position = [position["x"], position["y"], position["z"]]
        world_object.rotation = [rotation["x"], rotation["y"], rotation["z"]]
        world_object.scale = [scale["x"], scale["y"], scale["z"]]

        return world_object

    def to_json(self):
        return {
                    "worldObjectId": self.world_object_id,
                    "worldId": self.world_id,
                    "objectId": self.object_id,
                    "position": {
                        "x": self.position[0],
                        "y": self.position[1],
                        "z": self.position[2]
                    },
                    "rotation": {
                        "x": self.rotation[0],
                        "y": self.rotation[1],
                        "z": self.rotation[2]
                    },
                    "scale": {
                        "x": self.scale[0],
                        "y": self.scale[1],
                        "z": self.scale[2]
                    },
                }


