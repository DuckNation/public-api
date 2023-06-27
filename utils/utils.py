import typing
import uuid

import pymongo
from fastapi import Request, Query, Depends, HTTPException

if typing.TYPE_CHECKING:
    from api.info.Player import Player

from database import MongoSingleton


def get_param_from_request(param_name: str, request: Request):
    return request.query_params.get(param_name, "")


async def get_mongo_instance() -> pymongo.MongoClient:
    return await MongoSingleton.get_instance()


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
    if isinstance(uid, str):
        try:
            uid = format_uuid(uid)
        except ValueError:
            pass
        if len(uid) == 36:  # uuid
            stats = await instance.minecraft.users.find_one({"_id": uid})
        else:
            stats = await instance.minecraft.users.find_one({"username": uid})
    else:
        stats = await instance.minecraft.users.find_one({"uid": uid})

    if not stats:
        raise HTTPException(status_code=404, detail="User not found.")

    from api.info.Player import Player

    return Player(**stats)
