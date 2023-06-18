from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.websockets import WebSocket

from database import RedisSingleton


async def verify_ws_api_key(websocket: WebSocket, redis=Depends(RedisSingleton.get_instance)):
    api_key = None
    print(websocket.query_params)
    if "key" in websocket.query_params:
        api_key = websocket.query_params["key"]

    if api_key is None:
        if "Authorization" in websocket.headers:
            header_value = websocket.headers["Authorization"]
            if header_value.startswith("Bearer "):
                api_key = header_value.split(" ")[-1]

    if api_key is None:
        raise HTTPException(status_code=403, detail="API key not found")

    if not await is_valid_api_key(api_key, redis):
        raise HTTPException(status_code=403, detail="Invalid API key")

    return api_key


async def is_valid_api_key(api_key: str, redis):
    result = await redis.sismember("api-keys", api_key)
    return result


async def verify_http_api_key(request: Request, redis=Depends(RedisSingleton.get_instance)):
    api_key = None
    print(request.query_params)
    if "key" in request.query_params:
        api_key = request.query_params["key"]

    if api_key is None:
        if "Authorization" in request.headers:
            header_value = request.headers["Authorization"]
            if header_value.startswith("Bearer "):
                api_key = header_value.split(" ")[-1]

    if api_key is None:
        raise HTTPException(status_code=403, detail="API key not found")

    if not await is_valid_api_key(api_key, redis):
        raise HTTPException(status_code=403, detail="Invalid API key")

    return api_key
