from app.models.world_objects import WorldObject

def world_object_to_dict(world_object: WorldObject):
    return {
                "worldObjectId": world_object.world_object_id,
                "worldId": world_object.world_id,
                "objectId": world_object.object_id,
                "position": {
                    "x": world_object.position[0],
                    "y": world_object.position[1],
                    "z": world_object.position[2]
                },
                "rotation": {
                    "x": world_object.rotation[0],
                    "y": world_object.rotation[1],
                    "z": world_object.rotation[2]
                },
                "scale": {
                    "x": world_object.scale[0],
                    "y": world_object.scale[1],
                    "z": world_object.scale[2]
                },
           }

def create_load_world_message(world_objects: list[WorldObject]):
    return {
                "type": "loadWorld",
                "worldId": world_objects[0].world_id,
                "objects": [world_object_to_dict(obj) for obj in world_objects]
           }

    
