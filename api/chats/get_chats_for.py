from typing import Optional

import pymongo
from fastapi import APIRouter, Depends

from utils.utils import format_uuid_args, get_mongo_instance

router = APIRouter()


@router.get("/get", status_code=200, description="Get a list of chats.")
async def get_endpoint(
    uuid: Optional[str] = None,
    chat_uuid: Optional[str] = None,
    uuid_or_id: Optional[bool] = True,  # True = uuid, False = id
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    chats = []

    if uuid:
        uuid = format_uuid_args(uuid)
        uuid = uuid.upper().replace("-", "")
        query = {"players": {"$in": [uuid]}}
        results = instance.minecraft.chats.find(query)
    else:
        if chat_uuid:
            try:
                chat_uuid = format_uuid_args(chat_uuid)
                return await instance.minecraft.chats.find_one({"_id": chat_uuid})
            except ValueError:
                return await instance.minecraft.chats.find_one(
                    {"name": chat_uuid.lower().replace(" ", "-")}
                )
        else:
            results = instance.minecraft.chats.find()

    async for result in results:
        if uuid_or_id:
            chats.append({result["name"]: result["_id"]})
        else:
            chats.append(
                {result["_id"]: result["discordId"] if "discordId" in result else None}
            )
    print(chats)

    return chats


@router.get("/better-get", status_code=200, description="Get a list of chats.")
async def better_get_endpoint(
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
    chat_uuid: Optional[str] = None,
):
    if chat_uuid:
        try:
            chat_uuid = format_uuid_args(chat_uuid)
            return await instance.minecraft.chats.find_one({"_id": chat_uuid})
        except ValueError:
            return await instance.minecraft.chats.find_one(
                {"name": chat_uuid.lower().replace(" ", "-")}
            )
    else:
        chats = []
        results = instance.minecraft.chats.find()
        async for result in results:
            chats.append(
                {
                    "name": result["name"],
                    "uuid": result["_id"],
                    "discordId": result["discordId"] if "discordId" in result else None,
                }
            )
        return chats
