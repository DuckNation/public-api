import pymongo
from pydantic import BaseModel, Field


class Chat(BaseModel):
    uuid: str = Field(..., alias="_id")
    name: str
    owner: str
    players: list[str] = []
    password: str | None = None
    blocked_players: list[str] = Field(..., alias="blockedPlayers")
    discord_id: int | None = Field(..., alias="discordId")

    def dict(self, *args, **kwargs):
        return super().dict(by_alias=True)

    async def save(self, instance: pymongo.MongoClient):
        data = self.dict()
        from utils.utils import format_uuid
        uuid = format_uuid(data.get("_id"))  # should be already formatted, but just in case

        if uuid:
            await instance.minecraft.chats.replace_one({"_id": uuid}, data, upsert=True)
        else:
            raise ValueError("Chat does not have a valid UUID.")

    class Config:
        arbitrary_types_allowed = True
