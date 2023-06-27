import pymongo
from fastapi import Depends

from api.info.Player import Player
from utils.APIRouter import APIRouter
from utils.utils import get_mongo_instance, get_user_object

router = APIRouter()


@router.get("/settings", status_code=200, response_model=dict)
async def get_settings(
    player: Player = Depends(get_user_object),
):
    return player.settings


@router.patch("/settings", status_code=200, response_model=dict)
async def set_settings(
    settings: dict,
    player: Player = Depends(get_user_object),
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    player.settings = settings
    await player.save(instance)

    return player.settings


@router.put("/settings", status_code=200, response_model=dict)
async def set_setting(
    setting: str,
    value: str,
    player: Player = Depends(get_user_object),
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    player.settings[setting] = value
    await player.save(instance)

    return player.settings


@router.delete("/settings", status_code=200, response_model=dict)
async def delete_setting(
    setting: str,
    player: Player = Depends(get_user_object),
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    if setting in player.settings:
        del player.settings[setting]
    await player.save(instance)

    return player.settings
