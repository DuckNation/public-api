import pymongo
from fastapi import APIRouter, HTTPException, Depends

from api.chats.Chat import Chat
from utils.utils import get_mongo_instance, format_uuid_args

router = APIRouter()


@router.put(
    "/block",
    status_code=200,
    response_model=Chat,
    description="Block a player from a chat.",
)
async def block_endpoint(
    # name: str,
    victim: str,
    uuid: str,
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    try:
        victim, uuid = format_uuid_args(victim, uuid)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"<red>{e}")
    exists = await instance["happy"]["chats"].find_one({"owner": uuid})
    if not exists:
        raise HTTPException(
            status_code=404,  # todo refactor to add support to manage channels later
            detail=f"<red>You do not appear to own a chat.",
        )
    chat = Chat(**exists)

    if chat.owner != uuid:
        raise HTTPException(
            status_code=400,
            detail=f"<red>You can only (currently) run this command on your own chat.",
        )
    if victim == uuid:
        raise HTTPException(status_code=400, detail=f"<red>You cannot block yourself.")
    if victim in chat.players:
        chat.players.remove(victim)
    if victim not in chat.blocked_players:
        chat.blocked_players.append(victim)

    await instance.happy.chats.replace_one(
        {"_id": exists["_id"]}, chat.dict(by_alias=True), upsert=True
    )
    return chat
