import string
import secrets
from app.database.session import create_postgres_session

characters = string.ascii_uppercase + string.digits
def generate_id(model, id_column):
    with create_postgres_session() as session:
        characters = string.ascii_letters + string.digits
        while True:
            random_id = "".join(secrets.choice(characters) for _ in range(10))
            res = session.query(model).filter(id_column == random_id).first()
            if not res:
                return random_id

        

