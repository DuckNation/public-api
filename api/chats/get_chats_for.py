from typing import Optional

from fastapi import APIRouter

from database import MongoSingleton

router = APIRouter()


@router.get("/get", status_code=200)
async def get_endpoint(uuid: Optional[str]):
    instance = await MongoSingleton.get_instance()
    if uuid:
        uuid = uuid.upper().replace("-", "")
        query = {"players": {"$in": [uuid]}}
        results = instance.minecraft.chats.find(query)
        chats = []

        async for result in results:
            chats.append({result['name']: result['_id']})

    else:
        results = instance.minecraft.chats.find()
        chats = []

        async for result in results:
            chats.append({result['name']: result['_id']})

    return chats
