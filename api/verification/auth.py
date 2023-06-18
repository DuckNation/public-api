from fastapi import Depends, HTTPException
from starlette.exceptions import WebSocketException
from starlette.requests import Request
from starlette.websockets import WebSocket

from database import RedisSingleton


async def verify_ws_api_key(websocket: WebSocket, redis=Depends(RedisSingleton.get_instance)):
    api_key = await get_api_key(websocket)

    if api_key is None:
        raise WebSocketException(code=1008, reason="API key not found")
    if not await is_valid_api_key(api_key, redis):
        raise WebSocketException(code=1008, reason="Invalid API key")

    return api_key


async def get_api_key(req: WebSocket | Request) -> str | None:
    api_key = None
    if "key" in req.query_params:
        api_key = req.query_params["key"]

    if api_key is None:
        if "Authorization" in req.headers:
            header_value = req.headers["Authorization"]
            if header_value.startswith("Bearer "):
                api_key = header_value.split(" ")[-1]

    return api_key


async def is_valid_api_key(api_key: str, redis):
    result = await redis.sismember("api-keys", api_key)
    return result


async def verify_http_api_key(request: Request, redis=Depends(RedisSingleton.get_instance)):
    api_key = await get_api_key(request)

    if api_key is None:
        raise HTTPException(status_code=403, detail="API key not found")

    if not await is_valid_api_key(api_key, redis):
        raise HTTPException(status_code=403, detail="Invalid API key")

    return api_key
