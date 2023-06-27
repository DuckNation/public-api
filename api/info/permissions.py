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
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    player.permissions = []
    await player.save(instance)
    return player.permissions


@router.patch("/permissions", status_code=200, response_model=list[str])
async def add_permission(
    permission: str,
    player: Player = Depends(get_user_object),
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    if permission not in player.permissions:
        player.permissions.append(permission)
        await player.save(instance)
    return player.permissions