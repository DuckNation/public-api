import pymongo
from fastapi import APIRouter, HTTPException, Depends

from utils.utils import format_uuid_args, get_mongo_instance

router = APIRouter()


@router.delete("/delete", status_code=200, description="Delete a chat.")
async def delete_endpoint(
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

    if exists["owner"] != uuid:
        raise HTTPException(
            status_code=400, detail=f"<red>You cannot delete a chat you do not own."
        )

    await instance.minecraft.chats.delete_one({"_id": exists["_id"]})
    return {"message": f"You have deleted the chat <yellow>{name}</yellow>."}
