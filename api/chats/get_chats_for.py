from typing import Optional

import pymongo
from fastapi import APIRouter, Depends

from utils.utils import format_uuid_args, get_mongo_instance

router = APIRouter()


@router.get("/get", status_code=200)
async def get_endpoint(
    uuid: Optional[str] = None,
    chat_uuid: Optional[str] = None,
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    if uuid:
        uuid = format_uuid_args(uuid)
        uuid = uuid.upper().replace("-", "")
        query = {"players": {"$in": [uuid]}}
        results = instance.minecraft.chats.find(query)
        chats = []

        async for result in results:
            chats.append({result["name"]: result["_id"]})

    else:
        if chat_uuid:
            chat_uuid = format_uuid_args(chat_uuid)
            results = instance.minecraft.chats.find({"_id": chat_uuid})
        else:
            results = instance.minecraft.chats.find()
        chats = []

        async for result in results:
            chats.append(result)

    return chats
