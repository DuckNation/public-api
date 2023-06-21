from typing import Optional
from uuid import uuid4

import pymongo
from fastapi import APIRouter, HTTPException, Depends

from api.chats.Chat import Chat
from database import MongoSingleton
from utils.utils import format_uuid_args, get_mongo_instance

router = APIRouter()


@router.post("/create", status_code=200, response_model=Chat)
async def create_endpoint(
    name: str,
    uuid: str,
    password: Optional[str] = None,
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    name = name.lower().replace(" ", "-")[0:20]  # Max length of 20
    uuid = format_uuid_args(uuid)
    exists = await instance.minecraft.chats.find_one({"name": name})
    if exists:
        raise HTTPException(
            status_code=400,
            detail=f"<red>A chat by the name of <yellow>{name}</yellow> already exists.",
        )

    if await instance.minecraft.chats.count_documents({"owner": uuid}) >= 1:
        raise HTTPException(status_code=400, detail=f"<red>You already own a chat.")

    _dict = {
        "_id": format_uuid_args(str(uuid4())),
        "name": name,
        "players": [uuid],
        "owner": uuid,
        "password": password,
        "blockedPlayers": [],
    }

    await instance.minecraft.chats.insert_one(_dict)
    return Chat(**_dict)
