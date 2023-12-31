import pymongo
from fastapi import APIRouter, Depends, HTTPException

from api.info.Player import Player
from utils.utils import get_mongo_instance

router = APIRouter()


@router.post("/verify", status_code=200, description="Verify a user.")
async def verify_endpoint(
    uid: int, pin: str, instance: pymongo.MongoClient = Depends(get_mongo_instance)
):
    exists = await instance.happy.users.find_one({"uid": uid})
    if exists:
        raise HTTPException(
            status_code=400,
            detail=f"Your Discord account is already verified as {exists['username']}.",
        )

    pin = pin.upper()
    entry = await instance.happy.users.find_one({"pin": pin})
    if not entry:
        raise HTTPException(status_code=404, detail="Pin not found.")
    entry["uid"] = uid
    del entry["pin"]
    entry["permissions"] = [f"lp user {entry['username']} parent add verified"]
    player = Player(**entry)
    await instance.happy.users.replace_one({"pin": pin}, player.dict(), upsert=True)
    return {
        "message": f"Verification successful. You are now verified as {entry['username']}."
    }


# todo make sure users are added to their chat endpoints
