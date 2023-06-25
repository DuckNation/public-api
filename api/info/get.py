import pymongo
from fastapi import HTTPException, Depends

from api.info import Player
from api.info.Player import Player
from utils.APIRouter import APIRouter
from utils.utils import format_uuid, get_mongo_instance

router = APIRouter()


@router.get("/stats", status_code=200, response_model=Player)
async def stats_endpoint(
        uid: int | str,
        instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
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
    print(stats)
    stats.pop("pin", None)
    return Player(**stats)
