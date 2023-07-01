import pymongo
from fastapi import Depends

from api.info.Player import Player
from utils.APIRouter import APIRouter
from utils.utils import get_user_object, get_mongo_instance

router = APIRouter()


@router.get("/stats", status_code=200, response_model=Player)
async def stats_endpoint(
    player: Player = Depends(get_user_object),
):
    return player


@router.put("/stats", status_code=200, response_model=Player)
async def update_endpoint(
    player: Player = Depends(get_user_object),
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
    loginTime: [int, None] = None,
    logoutTime: [int, None] = None,
    playTime: [int, None] = None,
):
    if loginTime is not None:
        player.login_time = loginTime
    if logoutTime is not None:
        player.logout_time = logoutTime
    if playTime is not None:
        player.play_time = playTime

    await player.save(instance)

    return player
