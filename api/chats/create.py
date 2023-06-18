from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from api.chats.Chat import Chat
from database import MongoSingleton

router = APIRouter()


@router.post("/create", status_code=200, response_model=Chat)
async def create_endpoint(name: str, uuid: str, password: Optional[str] = None):
    instance = await MongoSingleton.get_instance()
    uuid = uuid.upper().replace("-", "")
    exists = await instance.minecraft.chats.find_one({"name": name})
    if exists:
        raise HTTPException(status_code=400,
                            detail=f"<red>A chat by the name of <yellow>{name}</yellow> already exists.")

    if await instance.minecraft.chats.count_documents({"owner": uuid}) > 1:
        raise HTTPException(status_code=400, detail=f"<red>You already own a chat.")

    _dict = {
        "_id": str(uuid4()),
        "name": name,
        "players": [uuid],
        "owner": uuid,
        "password": password,
        "blocked": [],
    }

    await instance.minecraft.chats.insert_one(_dict)
    return Chat(**_dict)
