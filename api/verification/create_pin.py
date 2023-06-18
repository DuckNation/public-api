import random
import string

from fastapi import APIRouter, Response, Request

from database import MongoSingleton

router = APIRouter()


# limiter = Limiter(key_func=ok, default_limits=["2/5seconds"])


@router.post("/create-pin", status_code=200)
# @limiter.shared_limit(limit_value="2/10second", scope="verification")
async def create_pin(username: str, uuid: str, response: Response, request: Request):
    uuid = uuid.upper().replace("-", "")
    instance = await MongoSingleton.get_instance()
    exists = await instance.minecraft.users.find_one({"username": username})
    pin = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=5))
    data = {"username": username, "pin": pin, "_id": uuid}
    if exists:
        if 'pin' not in exists:
            response.status_code = 400
            return {"message": f"<red>Your username is already registered. Run "
                               f"<yellow><click:suggest_command:'/unverify'>/unverify</click></yellow> to "
                               f"unverify your account."}
        else:
            data['pin'] = exists['pin']
            del data['_id']
    await instance.minecraft.users.insert_one(data)
    return {"message": f"<yellow>Success. Go back to the discord server "
                       f"(<green>https://discord.quack.boo</green>) and type <aqua>.verify "
                       f"{data['pin']}</aqua> to verify your account.</yellow>"}
