from redis_om import HashModel
from app.redis_client.session import get_redis_session
from app.redis_client.models.world_object import WorldObject 

from redis_om import JsonModel, Field

class World(JsonModel):
    world_id: str = Field(primary_key=True)
    owner_player_id: str
    objects: list[WorldObject] 

