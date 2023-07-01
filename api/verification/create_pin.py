import random
import string

import pymongo
from fastapi import APIRouter, Depends, HTTPException

from utils.utils import get_mongo_instance, format_uuid

router = APIRouter()


# limiter = Limiter(key_func=ok, default_limits=["2/5seconds"])


@router.post(
    "/create-pin", status_code=200, description="Create a pin to verify your account."
)
# @limiter.shared_limit(limit_value="2/10second", scope="verification")
async def create_pin(
    username: str,
    uuid: str,
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    uuid = format_uuid(uuid)
    exists = await instance.minecraft.users.find_one({"username": username})
    pin = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    data = {"username": username, "pin": pin, "uuid": uuid}
    if exists:
        if "pin" not in exists:
            raise HTTPException(
                status_code=400,
                detail=f"<red>Your username is already registered. "
                f"Run <aqua>.unverify</aqua> on "
                f"discord to unverify!",
            )
        else:
            data["pin"] = pin
    await instance.minecraft.users.replace_one({"uuid": uuid}, data, upsert=True)
    return {
        "message": f"<yellow>Success! Go back to the discord server "
        f"(<click:open_url:'https://discord.quack.boo'><green>https://discord.quack.boo</green></click>) "
        f"and type <hover:show_text:'<gray>Copy to Clipboard!'><click:copy_to_clipboard:"
        f".verify {data['pin']}><aqua>.verify {data['pin']}</aqua></click></hover> "
        f"to verify your account.</yellow>"
    }
