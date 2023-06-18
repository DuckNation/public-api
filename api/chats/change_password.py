from typing import Optional

from fastapi import APIRouter, HTTPException

from api.chats.Chat import Chat
from database import MongoSingleton

router = APIRouter()


@router.put("/password", status_code=200, response_model=Chat)
async def password_endpoint(uuid: str, password: Optional[str] = None):
    instance = await MongoSingleton.get_instance()
    uuid = uuid.upper().replace("-", "")
    exists = await instance.minecraft.chats.find_one({"owner": uuid})
    if not exists:
        raise HTTPException(status_code=400, detail=f"<red>You don't appear to own a chat.")

    exists['password'] = password

    chat = Chat(**exists)

    await instance.minecraft.chats.replace_one({"_id": exists['_id']}, chat.dict(), upsert=True)
    return chat
