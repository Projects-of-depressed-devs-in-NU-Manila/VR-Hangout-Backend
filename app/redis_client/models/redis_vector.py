
from redis_om import EmbeddedJsonModel
from app.redis_client.session import redis 


class Vector3(EmbeddedJsonModel):
    x: float
    y: float
    z: float
