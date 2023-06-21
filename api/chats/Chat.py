from pydantic import BaseModel, Field


class Chat(BaseModel):
    uuid: str = Field(..., alias="_id")
    name: str
    owner: str
    players: list[str] = []
    password: str | None = None
    blocked_players: list[str] = Field(..., alias="blockedPlayers")

    def dict(self, *args, **kwargs):
        return super().dict(by_alias=True)
