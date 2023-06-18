from fastapi import APIRouter, HTTPException

from database import MongoSingleton

router = APIRouter()


@router.delete("/leave", status_code=200)
async def leave_endpoint(name: str, uuid: str):
    instance = await MongoSingleton.get_instance()
    uuid = uuid.upper().replace("-", "")
    exists = await instance.minecraft.chats.find_one({"name": name})
    if not exists:
        raise HTTPException(status_code=400,
                            detail=f"<red>A chat by the name of <yellow>{name}</yellow> does not exist.")

    if exists['owner'] == uuid:
        raise HTTPException(status_code=400, detail=f"<red>You cannot leave a chat you own.")

    if uuid in exists['players']:
        exists['players'].remove(uuid)

    await instance.minecraft.chats.replace_one({"_id": exists['_id']}, exists, upsert=True)
    return {"message": f"You have left the chat <yellow>{name}</yellow>."}
