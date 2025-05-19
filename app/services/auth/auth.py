from app.core.id_gen import generate_id
from app.core.exceptions import AlreadyExists
from app.models.credentials import Credential
from sqlalchemy.orm import Session

class AuthService:

    @staticmethod
    def create_credentials(session: Session, player_id: str, username: str, password: str):
        if session.query(Credential).filter(Credential.username == username).first():
            raise AlreadyExists("Username Already Exists")

        id =  generate_id(Credential, Credential.credential_id)
        credential = Credential(credential_id=id, username=username, password=password, player_id=player_id)
        session.add(credential)
        session.flush()
        return id
        


