from typing import Optional

from fastapi import APIRouter, HTTPException

from api.chats.Chat import Chat
from database import MongoSingleton

router = APIRouter()


@router.put("/set-discord", status_code=200, response_model=Chat)
async def discord_endpoint(chat_uuid: str, channel_id: int = None):
    instance = await MongoSingleton.get_instance()
    exists = await instance.minecraft.chats.find_one({"_id": chat_uuid})
    if not exists:
        raise HTTPException(status_code=400, detail=f"Chat doesn't seem to exist.")

    exists['discord_id'] = channel_id

    chat = Chat(**exists)

    await instance.minecraft.chats.replace_one({"_id": exists['_id']}, exists, upsert=True)
    return chat
