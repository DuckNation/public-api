from typing import Optional

from fastapi import APIRouter

from database import MongoSingleton

router = APIRouter()


@router.get("/get", status_code=200)
async def get_endpoint(uuid: Optional[str] = None, chat_uuid: Optional[str] = None):
    instance = await MongoSingleton.get_instance()
    if uuid:
        uuid = uuid.upper().replace("-", "")
        query = {"players": {"$in": [uuid]}}
        results = instance.minecraft.chats.find(query)
        chats = []

        async for result in results:
            chats.append({result['name']: result['_id']})

    else:
        if chat_uuid:
            results = instance.minecraft.chats.find({"_id": chat_uuid})
        else:
            results = instance.minecraft.chats.find()
        chats = []

        async for result in results:
            chats.append(result)

    return chats
