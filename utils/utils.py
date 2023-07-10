import typing
import uuid

import pymongo
import redis.asyncio
from fastapi import Request, Query, Depends, HTTPException

if typing.TYPE_CHECKING:
    from api.info.Player import Player
    from api.chats.Chat import Chat

from database import MongoSingleton, RedisSingleton


def get_param_from_request(param_name: str, request: Request):
    return request.query_params.get(param_name, "")


async def get_mongo_instance() -> pymongo.MongoClient:
    return await MongoSingleton.get_instance()


async def get_redis_instance() -> redis.asyncio.Redis:
    return await RedisSingleton.get_instance()


def format_uuid(uuid_str: str) -> str:
    return str(uuid.UUID(uuid_str)).upper()


def format_uuid_args(*args) -> list | str:
    if len(args) == 1:
        return format_uuid(args[0])
    return [format_uuid(arg) for arg in args]


async def get_user_object(
    uid: int | str = Query(...),
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
) -> "Player":
    from api.info.Player import Player

    if isinstance(uid, str):
        try:
            uid = format_uuid(uid)
        except ValueError:
            pass
        if len(uid) == 36:  # uuid
            stats = await instance.happy.users.find_one({"uuid": uid})
        else:
            stats = await instance.happy.users.find_one({"username": uid})
    else:
        stats = await instance.happy.users.find_one({"uid": uid})

    if not stats:
        raise HTTPException(status_code=404, detail="User not found.")

    from api.info.Player import Player

    """ code for creating a new user if not found
    - somehow make this merge the newly created uuid from create-pin and the alrady existing one
        if not stats:
        try:
            int(uid)
        except ValueError:
            raise HTTPException(status_code=404, detail="User not found.")
        else:
            player = Player(uid=uid)
            await player.save(instance)
            return player"""

    return Player(**stats)


async def get_chat_object(
    uid: int | str = Query(...),
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
) -> "Chat":
    if isinstance(uid, str):
        try:
            uid = format_uuid(uid)
        except ValueError:
            pass
        if len(uid) == 36:  # uuid
            stats = await instance.happy.chats.find_one({"_id": uid})
        else:
            stats = await instance.happy.chats.find_one({"name": uid})
    else:
        stats = await instance.happy.chats.find_one({"discordId": uid})

    if not stats:
        raise HTTPException(status_code=404, detail="Chat not found.")

    from api.chats.Chat import Chat

    return Chat(**stats)
