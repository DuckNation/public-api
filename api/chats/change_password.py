from typing import Optional

import pymongo
from fastapi import APIRouter, HTTPException, Depends

from api.chats.Chat import Chat
from utils.utils import get_mongo_instance, format_uuid_args

router = APIRouter()


@router.put("/password", status_code=200, response_model=Chat, description="Change the password of a chat.")
async def password_endpoint(
    uuid: str,
    password: Optional[str] = None,
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    uuid = format_uuid_args(uuid)
    exists = await instance.minecraft.chats.find_one({"owner": uuid})
    if not exists:
        raise HTTPException(
            status_code=400, detail=f"<red>You don't appear to own a chat."
        )

    chat = Chat(**exists)

    chat.password = password

    await instance.minecraft.chats.replace_one(
        {"_id": exists["_id"]}, chat.dict(), upsert=True
    )
    return chat
