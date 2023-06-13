from fastapi import APIRouter

from .ws import router as wss_router, redis_subscriptions, unsubscribe_redis_channel

router = APIRouter(prefix="/wss")


@router.on_event("shutdown")
async def shutdown_event():
    # Unsubscribe from all Redis channels on application shutdown
    for channel in redis_subscriptions:
        await unsubscribe_redis_channel(channel)


router.include_router(wss_router)
