from app.models.world_objects import WorldObject

class WorldData():
    type: str
    world_id: str
    objects: list[WorldObject] 

    def __init__(self, type: str = "", world_id: str = "", objects: list[WorldObject] = []):
        self.type = type
        self.world_id = world_id
        self.objects = objects
    
    def to_json(self):
        return {
                "type": self.type,
                "worldId": self.world_id,
                "objects": [obj.to_json() for obj in self.objects]
        }

    @staticmethod
    def from_json(json: dict):
        world_data = WorldData()
        world_data.type = json["type"]
        world_data.world_id = json["worldId"]

        world_data.objects = [WorldObject.from_json(obj) for obj in json["objects"]]

        return world_data

