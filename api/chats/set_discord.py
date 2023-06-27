import pymongo
from fastapi import APIRouter, HTTPException, Depends

from api.chats.Chat import Chat
from utils.utils import get_mongo_instance, format_uuid_args

router = APIRouter()


@router.put(
    "/set-discord",
    status_code=200,
    response_model=Chat,
    description="Set the discord channel of a chat.",
)
async def discord_endpoint(
    chat_uuid: str,
    channel_id: int = None,
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    exists = await instance.minecraft.chats.find_one(
        {"_id": format_uuid_args(chat_uuid)}
    )
    if not exists:
        raise HTTPException(status_code=400, detail=f"Chat doesn't seem to exist.")

    exists["discordId"] = channel_id

    chat = Chat(**exists)

    await instance.minecraft.chats.replace_one(
        {"_id": exists["_id"]}, exists, upsert=True
    )
    return chat
