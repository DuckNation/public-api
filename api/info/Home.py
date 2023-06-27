from pydantic import BaseModel


class Home(BaseModel):
    name: str
    dimension: str
    x: int
    y: int
    z: int
    tier: int
    owner: str
