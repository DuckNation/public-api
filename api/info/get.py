import pymongo
from fastapi import Depends

from api.info.Player import Player
from utils.APIRouter import APIRouter
from utils.utils import get_mongo_instance, get_user_object

router = APIRouter()


@router.get("/stats", status_code=200, response_model=Player)
async def stats_endpoint(
        player: Player = Depends(get_user_object),
        instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    return player
