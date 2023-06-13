import random
import string

from fastapi import APIRouter, Response

from database import MongoSingleton

router = APIRouter()


@router.post("/create-pin", status_code=200)
async def create_pin(username: str, uuid: str, response: Response):
    uuid = uuid.upper().replace("-", "")
    instance = await MongoSingleton.get_instance()
    exists = await instance.minecraft.users.find_one({"username": username})
    if exists:
        response.status_code = 400
        return {"message": f"<red>Your username is already registered. Run "
                           f"<yellow><click:suggest_command:'/unverify'>/unverify</click></yellow> to "
                           f"unverify your account."}
    pin = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=5))
    await instance.minecraft.users.insert_one({"username": username, "pin": pin, "_id": uuid})
    return {"message": f"<yellow>Success. Go back to the discord server "
                       f"(<green>https://discord.quack.boo</green>) and type <aqua>.verify "
                       f"{pin}</aqua> to verify your account.</yellow>"}
