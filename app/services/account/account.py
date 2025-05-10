from app.postgres_client.session import create_postgres_session
from app.postgres_client.models.players import Player
from app.core.id_gen import generate_id

class PlayerService:
    @staticmethod
    def create_account() -> str:
        with create_postgres_session() as session:
            id = generate_id()
            player = Player(player_id=id)
            session.add(player)
            session.commit()
            return id