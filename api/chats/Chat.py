from typing import List, Optional

from pydantic import BaseModel, Field


class Chat(BaseModel):
    uuid: str = Field(..., alias="_id")
    name: str
    owner: str
    players: List[str] = []
    password: Optional[str] = None
    blockedPlayers: List[str] = []
