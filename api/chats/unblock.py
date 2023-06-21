from fastapi import APIRouter, HTTPException

from api.chats.Chat import Chat
from database import MongoSingleton

router = APIRouter()


@router.put("/unblock", status_code=200, response_model=Chat)
async def unblock_endpoint(name: str, uuid: str, victim: str):
    instance = await MongoSingleton.get_instance()
    uuid = uuid.upper().replace("-", "")
    exists = await instance.minecraft.chats.find_one({"name": name})
    name = name.lower()
    if not exists:
        raise HTTPException(status_code=400,
                            detail=f"<red>A chat by the name of <yellow>{name}</yellow> does not exist.")

    if exists['owner'] != uuid:
        raise HTTPException(status_code=400, detail=f"<red>You can only run this command on your own chat.")

    if victim in exists['blocked']:
        exists['blocked'].remove(victim)

    chat = Chat(**exists)

    await instance.minecraft.chats.replace_one({"_id": exists['_id']}, chat.dict(), upsert=True)
    return chat
