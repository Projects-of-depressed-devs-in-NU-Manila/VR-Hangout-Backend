class World:
    world_id: str = ""
    player_ids: set[str]  = set()# ids of clients connected to this world

    def __init__(self, world_id: str, player_ids: list[str]):
        self.world_id = world_id
        self.player_ids = set(player_ids)