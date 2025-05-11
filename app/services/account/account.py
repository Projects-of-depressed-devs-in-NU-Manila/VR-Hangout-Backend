from app.database.session import create_postgres_session
from app.models.players import Player
from app.core.id_gen import generate_id

from sqlalchemy.orm import Session


class PlayerService:
    @staticmethod
    def create_account(session: Session) -> str:
        id = generate_id(Player, Player.player_id)
        player = Player(player_id=id)
        session.add(player)
        session.flush()
        return id
        