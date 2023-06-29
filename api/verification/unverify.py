import pymongo
from fastapi import APIRouter, Depends, HTTPException

from api.info.Player import Player
from utils.utils import get_mongo_instance, format_uuid, get_user_object

router = APIRouter()


@router.delete("/unverify", status_code=200, description="Unverify a user.")
async def unverify_endpoint(
    player: Player = Depends(get_user_object),
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    player.permissions.clear()
    saved_uuid = player.uuid
    player.pin = None
    player.uid = None

    await player.save(instance)

    results = instance.minecraft.chats.find({"players": {"$in": [player.uuid]}})
    chats = []

    async for result in results:
        chats.append({result["name"]: result["_id"]})

    return {"player_uuid": saved_uuid, "chats": chats}
