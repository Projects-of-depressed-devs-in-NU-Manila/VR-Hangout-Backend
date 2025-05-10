from app.core.id_gen import generate_id
from app.postgres_client.session import create_postgres_session
from app.postgres_client.models.credentials import Credential

class AuthService:

    @staticmethod
    def create_credentials(player_id: str, username: str, password: str):
        with create_postgres_session() as session:
            id =  generate_id()
            credential = Credential(credential_id=id, username=username, password=password, player_id=player_id)
            session.add(credential)
            session.commit()
            return id
            


