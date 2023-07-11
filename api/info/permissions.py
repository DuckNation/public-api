from typing import Optional

import pymongo
from fastapi import Depends

from api.info.Player import Player
from utils.APIRouter import APIRouter
from utils.utils import get_mongo_instance, get_user_object

router = APIRouter()


@router.get("/permissions", status_code=200, response_model=list[str])
async def get_permissions(
    player: Player = Depends(get_user_object),
):
    return player.permissions


@router.delete("/permissions", status_code=200, response_model=list[str])
async def clear_permissions(
    player: Player = Depends(get_user_object),
    permission: Optional[str] = None,
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    if permission:
        if permission in player.permissions:
            player.permissions.remove(permission)
    else:
        player.permissions = []
    await player.save(instance)
    return player.permissions


@router.patch("/permissions", status_code=200, response_model=list[str])
async def add_permission(
    permission: str,
    player: Player = Depends(get_user_object),
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    permission.replace("{username}", player.username)
    permission.replace("{uuid}", player.uuid)
    permission.replace("{uid}", str(player.uid))
    permission.replace("{pin}", player.pin)

    if permission not in player.permissions:
        player.permissions.append(permission)
        await player.save(instance)
    return player.permissions
