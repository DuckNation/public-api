from typing import List, Optional

import pymongo
from pydantic import BaseModel, Field

from api.info.Home import Home


class Player(BaseModel):
    uuid: Optional[str] = None
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
    permissions: List[str] = []

    server_stats: dict[str, str | int] = Field({}, alias="serverStats")

    def dict(self, *args, **kwargs):
        return super().dict(by_alias=True)

    async def save(self, instance: pymongo.MongoClient):
        data = self.dict()

        if data["uuid"]:
            from utils.utils import format_uuid

            uuid = format_uuid(
                data.get("uuid")
            )  # should be already formatted, but just in case
            await instance.happy.users.replace_one({"uuid": uuid}, data, upsert=True)

        else:
            await instance.happy.users.replace_one({"uid": self.uid}, data, upsert=True)

    @property
    def exists(self) -> bool:
        return self.uuid is not None

    class Config:
        arbitrary_types_allowed = True
