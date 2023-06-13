from fastapi import APIRouter, Response

from database import MongoSingleton

router = APIRouter()


@router.post("/verify", status_code=200)
async def verify_endpoint(uid: int, pin: str, response: Response):
    instance = await MongoSingleton.get_instance()
    pin = pin.upper()
    entry = await instance.minecraft.users.find_one({"pin": pin})
    if not entry:
        response.status_code = 400
        return {"message": f"{pin} isn't a valid pin."}
    entry["uid"] = uid
    del entry["pin"]
    await instance.minecraft.users.replace_one({"pin": pin}, entry, upsert=True)
    return {"message": f"Verification successful. You are now verified as {entry['username']}."}
