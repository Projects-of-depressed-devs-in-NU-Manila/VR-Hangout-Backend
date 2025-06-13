from app.core.id_gen import generate_id
from app.core.exceptions import AlreadyExists, DoesNotExists, MismatchException
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
        return credential

    @staticmethod
    def signin(session: Session, username: str, password: str):
        credential = session.query(Credential).filter(Credential.username == username).first()

        if credential is None:
            raise DoesNotExists("Player with that name does not exists")
        
        if not str(credential.password) == password:
            raise  MismatchException("Password is incorrect")

        return credential
    


         
        


