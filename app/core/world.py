class World:
    world_id: str = ""
    cliend_ids: set[str]  = set()# ids of clients connected to this world

    def __init__(self, world_id: str, cliend_ids: list[str]):
        self.world_id = world_id
        self.cliend_ids = set(cliend_ids)