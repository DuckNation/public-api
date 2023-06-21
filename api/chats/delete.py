from fastapi import APIRouter, HTTPException

from database import MongoSingleton

router = APIRouter()


@router.delete("/delete", status_code=200)
async def delete_endpoint(name: str, uuid: str):
    instance = await MongoSingleton.get_instance()
    uuid = uuid.upper().replace("-", "")
    name = name.lower()
    exists = await instance.minecraft.chats.find_one({"name": name})
    if not exists:
        raise HTTPException(status_code=400,
                            detail=f"<red>A chat by the name of <yellow>{name}</yellow> does not exist.")

    if exists['owner'] != uuid:
        raise HTTPException(status_code=400, detail=f"<red>You cannot delete a chat you do not own.")

    await instance.minecraft.chats.delete_one({"_id": exists['_id']})
    return {"message": f"You have deleted the chat <yellow>{name}</yellow>."}