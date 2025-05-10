import string
import secrets

characters = string.ascii_uppercase + string.digits
def generate_id(len: int = 10):
    random_id = "".join(secrets.choice(characters) for _ in range(len))
    return random_id

