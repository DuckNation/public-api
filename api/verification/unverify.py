import pymongo
from fastapi import APIRouter, Depends, HTTPException

from utils.utils import get_mongo_instance, format_uuid

router = APIRouter()


@router.delete("/unverify", status_code=200)
async def unverify_endpoint(
        uid: int | str,
        instance: pymongo.MongoClient = Depends(get_mongo_instance),

):
    try:
        int(uid)
    except ValueError:
        raise HTTPException(status_code=400, detail="You may only run this command on Discord!")

    username = await instance.minecraft.users.find_one({"uid": uid})
    if not username:
        raise HTTPException(status_code=404, detail="You aren't verified.")
    uuid = format_uuid(username["_id"])

    await instance.minecraft.users.update_one({"uid": uid}, {"$unset": {"uid": ""}})
    results = instance.minecraft.chats.find({"players": {"$in": [uuid]}})
    chats = []

    async for result in results:
        chats.append({result["name"]: result["_id"]})

    return chats
