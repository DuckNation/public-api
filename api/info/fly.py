import pymongo
from fastapi import Depends

from api.info.Player import Player
from utils.APIRouter import APIRouter
from utils.utils import get_mongo_instance, get_user_object

router = APIRouter()


@router.get("/fly", status_code=200, response_model=dict)
async def get_fly_time(
        player: Player = Depends(get_user_object),
        instance: pymongo.MongoClient = Depends(get_mongo_instance)
):
    return {
        "flyTime": player.fly_time,
        "message": f"{player.username} has {player.fly_time} seconds of fly time left."
    }


@router.put("/fly", status_code=200, response_model=dict)
async def set_fly_time(
        player: Player = Depends(get_user_object),
        time: int = -1,
        instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    player.fly_time = time
    await player.save(instance)

    return {
        "flyTime": player.fly_time,
        "message": f"{player.username}'s fly time has been set to {player.fly_time} seconds!"
    }

