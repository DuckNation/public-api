from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from api.verification import router as verification_router
from api.wss import router as wss_router
from database import RedisSingleton
from utils.APIRouter import APIRouter
from .verification import verify, create_pin, unverify

router = APIRouter(prefix="/api", tags=["Protected API"])

api_key_header = APIKeyHeader(name="Authorization")


async def is_valid_api_key(api_key: str, redis):
    result = await redis.sismember("api-keys", api_key)
    return result


async def verify_api_key(api_key: str = Depends(api_key_header), redis=Depends(RedisSingleton.get_instance)):
    api_key = api_key.split(" ")[-1]
    if not await is_valid_api_key(api_key, redis):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key


router.include_router(verification_router)
router.include_router(wss_router, dependencies=[Depends(verify_api_key)])
