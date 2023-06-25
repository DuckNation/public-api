from typing import List, Optional

from pydantic import BaseModel, Field


class Player(BaseModel):
    uuid: str = Field(..., alias="_id")
    username: str
    uid: Optional[int]
    pin: Optional[str]
    saved_homes: List[str] = Field([], alias="savedHomes")
    last_location: dict[str, str] = Field({}, alias="lastLocation")
    login_time: int = Field(-1, alias="loginTime")
    logout_time: int = Field(-1, alias="logoutTime")
    play_time: int = Field(-1, alias="playTime")
    permissions: list[str] = Field([], alias="permissions")
    settings: dict[str, str | int] = Field({}, alias="settings")

    server_stats: dict[str, str | int] = Field({}, alias="serverStats")

    def dict(self, *args, **kwargs):
        return super().dict(by_alias=True)
