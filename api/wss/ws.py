import asyncio
import uuid

import async_timeout
from redis.asyncio.client import PubSub
from starlette.websockets import WebSocket, WebSocketDisconnect

from database import RedisSingleton
from utils.APIRouter import APIRouter

router = APIRouter()

redis_subscriptions: dict[str, PubSub] = {}
websocket_clients: set["Client"] = set()


class Client:
    def __init__(self, websocket: WebSocket, channel):
        self.id = str(uuid.uuid4())
        self.websocket = websocket
        self.channel = channel


async def subscribe_redis_channel(channel):
    if channel not in redis_subscriptions:
        pubsub = (await RedisSingleton.get_instance()).pubsub()
        await pubsub.subscribe(channel)
        redis_subscriptions[channel] = pubsub
        asyncio.create_task(process_redis_messages(channel))


async def process_redis_messages(channel):
    subscription = redis_subscriptions[channel]
    while True:
        try:
            async with async_timeout.timeout(0.01):
                message = await subscription.get_message(ignore_subscribe_messages=True)
                if message:
                    decoded_message = bytes(message["data"]).decode("utf-8")
                    parts = decoded_message.rsplit(":", maxsplit=1)

                    if len(parts) == 2:
                        await send_message_to_clients(channel, parts[0], parts[1])
                    else:
                        print("Invalid message received: " + decoded_message)
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass
        finally:
            if channel not in [c.channel for c in websocket_clients]:
                await unsubscribe_redis_channel(channel)
                break


async def send_message_to_clients(channel, message, sender):
    clients = [client for client in websocket_clients if client.channel == channel if client.id != sender]
    for client in clients:
        await client.websocket.send_text(message)


async def unsubscribe_redis_channel(channel):
    subscription = redis_subscriptions.pop(channel, None)
    if subscription:
        await subscription.unsubscribe(channel)


@router.websocket("/{channel}")
async def websocket_endpoint(channel: str, websocket: WebSocket):
    await websocket.accept()
    client = Client(websocket, channel)
    websocket_clients.add(client)
    await subscribe_redis_channel(channel)
    try:
        instance = await RedisSingleton.get_instance()
        while True:
            data = await websocket.receive_text()
            await instance.publish(channel, data + ":" + client.id)
    except WebSocketDisconnect:
        pass
    finally:
        websocket_clients.remove(client)
        if channel not in [c.channel for c in websocket_clients]:
            await unsubscribe_redis_channel(channel)
