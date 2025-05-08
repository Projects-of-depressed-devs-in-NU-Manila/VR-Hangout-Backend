from pydantic import BaseModel

class Vector3(BaseModel):
    x: float = 0
    y: float = 0
    z: float = 0

