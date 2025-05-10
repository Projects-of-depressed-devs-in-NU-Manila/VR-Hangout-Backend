from redis_om import EmbeddedJsonModel
from app.redis_client.models.redis_vector import Vector3

class WorldObject(EmbeddedJsonModel):
    object_id: str
    position: Vector3
    rotation: Vector3
    scale: Vector3

