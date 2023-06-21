from typing import Optional

from fastapi import APIRouter, HTTPException

from api.chats.Chat import Chat
from database import MongoSingleton

router = APIRouter()


@router.post("/join", status_code=200, response_model=Chat)
async def join_endpoint(name: str, uuid: str, password: Optional[str] = None):
    instance = await MongoSingleton.get_instance()
    uuid = uuid.upper().replace("-", "")
    name = name.lower()
    exists = await instance.minecraft.chats.find_one({"name": name})
    if not exists:
        raise HTTPException(status_code=400,
                            detail=f"<red>A chat by the name of <yellow>{name}</yellow> does not exist.")

    if uuid in exists['players'] or exists['owner'] == uuid:
        raise HTTPException(status_code=400, detail=f"<red>You are already in this chat.")

    if exists['password'] and exists['password'] != password:
        raise HTTPException(status_code=400, detail=f"<red>The password you entered is incorrect.")

    exists['players'].append(uuid)

    chat = Chat(**exists)

    await instance.minecraft.chats.replace_one({"_id": exists['_id']}, chat.dict(), upsert=True)
    return chat
