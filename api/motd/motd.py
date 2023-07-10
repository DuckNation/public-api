import redis.asyncio
from fastapi import APIRouter, Depends

from utils.utils import get_redis_instance

router = APIRouter()


@router.get("/", status_code=200)
async def get_endpoint(
    ip_address: str, instance: redis.asyncio.Redis = Depends(get_redis_instance)
):
    res = await instance.get(f"motd:{ip_address}")

    return {
        "found": True if res is not None else False,
        "username": res.decode("utf-8") if res is not None else "",
    }


@router.post("/", status_code=200, description="Verify a user.")
async def set_endpoint(
    ip_address: str,
    username: str,
    instance: redis.asyncio.Redis = Depends(get_redis_instance),
):
    await instance.set(f"motd:{ip_address}", username)

    return {
        "message": f"Set MOTD for {ip_address} to {username}.",
        "username": username,
    }
