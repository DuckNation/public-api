from typing import Optional

import pymongo
from fastapi import APIRouter, HTTPException, Depends

from api.chats.Chat import Chat
from utils.utils import format_uuid_args, get_mongo_instance

router = APIRouter()


@router.post("/join", status_code=200, response_model=Chat, description="Join a chat.")
async def join_endpoint(
    name: str,
    uuid: str,
    password: Optional[str] = None,
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    uuid = format_uuid_args(uuid)
    name = name.lower().replace(" ", "-")[0:20]  # Max length of 20
    exists = await instance.happy.chats.find_one({"name": name})
    if not exists:
        raise HTTPException(
            status_code=400,
            detail=f"<red>A chat by the name of <yellow>{name}</yellow> does not exist.",
        )

    if uuid in exists["players"]:
        raise HTTPException(
            status_code=400, detail=f"<red>You are already in this chat."
        )

    if exists["password"] and exists["password"] != password:
        raise HTTPException(
            status_code=400, detail=f"<red>The password you entered is incorrect."
        )

    exists["players"].append(uuid)

    chat = Chat(**exists)

    await instance.happy.chats.replace_one(
        {"_id": exists["_id"]}, chat.dict(), upsert=True
    )
    return chat
