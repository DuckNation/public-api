import pymongo
from fastapi import APIRouter, HTTPException, Depends

from utils.utils import get_mongo_instance, format_uuid_args

router = APIRouter()


@router.delete("/leave", status_code=200)
async def leave_endpoint(
    name: str,
    uuid: str,
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    uuid = format_uuid_args(uuid)
    name = name.lower().replace(" ", "-")[0:20]  # Max length of 20
    exists = await instance.minecraft.chats.find_one({"name": name})
    if not exists:
        raise HTTPException(
            status_code=400,
            detail=f"<red>A chat by the name of <yellow>{name}</yellow> does not exist.",
        )

    if exists["owner"] == uuid:
        raise HTTPException(
            status_code=400, detail=f"<red>You cannot leave a chat you own."
        )

    if uuid in exists["players"]:
        exists["players"].remove(uuid)

    await instance.minecraft.chats.replace_one(
        {"_id": exists["_id"]}, exists, upsert=True
    )
    return {"message": f"You have left the chat <yellow>{name}</yellow>."}
