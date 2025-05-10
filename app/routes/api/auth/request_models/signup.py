
from pydantic import BaseModel

class SignupBody(BaseModel):
    username :str
    password :str