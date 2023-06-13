from database import MongoSingleton
from utils.APIRouter import APIRouter

router = APIRouter()


@router.delete("/unverify", status_code=200)
async def unverify_endpoint(uid: int | str):
    instance = await MongoSingleton.get_instance()
    if isinstance(uid, str):
        await instance.minecraft.users.delete_one({"username": uid})
        return {"message": "<green>Unverification successful"}
    else:
        await instance.minecraft.users.delete_one({"uid": uid})
        return {"message": "Unverification successful"}
