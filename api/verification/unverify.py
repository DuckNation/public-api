import pymongo
from fastapi import APIRouter, Depends, HTTPException

from utils.utils import get_mongo_instance, format_uuid

router = APIRouter()


@router.delete("/unverify", status_code=200)
async def unverify_endpoint(
        uid: int | str,
        instance: pymongo.MongoClient = Depends(get_mongo_instance),

):
    raise HTTPException(status_code=404, detail="This endpoint is currently disabled.")
    # todo remove from chat channels before finishing unverify
    # if isinstance(uid, str):
    #     uid = format_uuid(uid)
    #     await instance.minecraft.users.delete_one({"_id": uid})
    #     return {"message": "<green>Unverification successful"}
    # else:
    #     await instance.minecraft.users.delete_one({"uid": uid})
    #     return {"message": "Unverification successful"}
