import pymongo
from fastapi import APIRouter, Depends, HTTPException

from api.info.Player import Player
from utils.utils import get_mongo_instance, format_uuid

router = APIRouter()


@router.delete("/unverify", status_code=200, description="Unverify a user.")
async def unverify_endpoint(
    uid: int | str,
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    try:
        int(uid)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="You may only run this command on Discord!"
        )

    player = await instance.minecraft.users.find_one({"uid": uid})
    if not player:
        raise HTTPException(status_code=404, detail="You aren't verified.")

    player_obj = Player(**player)
    player_obj.permissions.clear()
    player_obj.pin = None
    player_obj.uid = None
    uuid = format_uuid(player["_id"])

    await instance.minecraft.users.replace_one(
        {"uid": uid}, player_obj.dict(), upsert=True
    )
    results = instance.minecraft.chats.find({"players": {"$in": [uuid]}})
    chats = []

    async for result in results:
        chats.append({result["name"]: result["_id"]})

    return chats
