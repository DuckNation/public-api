import pymongo
from fastapi import APIRouter, HTTPException, Depends

from api.chats.Chat import Chat
from utils.utils import get_mongo_instance, format_uuid_args

router = APIRouter()


@router.put(
    "/unblock",
    status_code=200,
    response_model=Chat,
    description="Unblock a user from a chat.",
)
async def unblock_endpoint(
    name: str,
    uuid: str,
    victim: str,
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    uuid = format_uuid_args(uuid)
    exists = await instance.happy.chats.find_one({"name": name})
    name = name.lower()
    if not exists:
        raise HTTPException(
            status_code=400,
            detail=f"<red>A chat by the name of <yellow>{name}</yellow> does not exist.",
        )

    if exists["owner"] != uuid:
        raise HTTPException(
            status_code=400,
            detail=f"<red>You can only run this command on your own chat.",
        )

    if victim in exists["blocked"]:
        exists["blocked"].remove(victim)

    chat = Chat(**exists)

    await instance.happy.chats.replace_one(
        {"_id": exists["_id"]}, chat.dict(), upsert=True
    )
    return chat
