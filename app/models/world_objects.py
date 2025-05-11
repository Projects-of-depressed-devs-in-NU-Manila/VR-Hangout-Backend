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


