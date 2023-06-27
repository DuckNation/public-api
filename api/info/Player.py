from typing import List, Optional

import pymongo
from pydantic import BaseModel, Field

from api.info.Home import Home


class Player(BaseModel):
    uuid: Optional[str] = Field(None, alias="_id")
    username: Optional[str] = None
    uid: Optional[int] = None
    pin: Optional[str] = None
    saved_homes: List[Home] = Field([], alias="savedHomes")
    last_location: dict[str, str] = Field({}, alias="lastLocation")
    login_time: int = Field(-1, alias="loginTime")
    logout_time: int = Field(-1, alias="logoutTime")
    play_time: int = Field(-1, alias="playTime")
    settings: dict[str, str | int] = {}
    fly_time: int = Field(-1, alias="flyTime")

    server_stats: dict[str, str | int] = Field({}, alias="serverStats")

    def dict(self, *args, **kwargs):
        return super().dict(by_alias=True)

    async def save(self, instance: pymongo.MongoClient):
        data = self.dict()
        uuid = data.get("_id")

        if uuid:
            await instance.minecraft.users.replace_one({"_id": uuid}, data, upsert=True)
        else:
            raise ValueError("Player does not have a valid UUID.")

    @property
    def exists(self) -> bool:
        return self.uuid is not None

    class Config:
        arbitrary_types_allowed = True
