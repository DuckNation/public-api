import asyncio

from fastapi import websockets

from database import MongoSingleton, RedisSingleton
from utils.APIRouter import APIRouter

router = APIRouter()

redis_subscriptions = {}
websocket_clients = set()


class Client:
    def __init__(self, websocket, channel):
        self.websocket = websocket
        self.channel = channel


async def subscribe_redis_channel(channel):
    if channel not in redis_subscriptions:
        subscription = await( (await RedisSingleton.get_instance()).pubsub()).subscribe(channel)
        print(f"Subscribed to Redis channel: {channel}")
        print(subscription)
        redis_subscriptions[channel] = subscription
        asyncio.create_task(process_redis_messages(channel))


async def process_redis_messages(channel):
    subscription = redis_subscriptions[channel]
    while await subscription[0].wait_message():
        message = await subscription[0].get(encoding="utf-8")
        await send_message_to_clients(channel, message)


async def send_message_to_clients(channel, message):
    clients = [client for client in websocket_clients if client.channel == channel]
    for client in clients:
        await client.websocket.send(message)


async def unsubscribe_redis_channel(channel):
    global redis_subscriptions
    subscription = redis_subscriptions.pop(channel, None)
    if subscription is not None:
        await subscription[0].unsubscribe(channel)


@router.websocket("/ws/{channel}")
async def ws_handler(websocket: websockets.WebSocket, channel: str):
    await websocket.accept()
    client = Client(websocket, channel)
    websocket_clients.add(client)
    await subscribe_redis_channel(channel)
    try:
        while True:
            message = await websocket.receive()
            print(f"Received message from client: {message}")
    except Exception:
        pass
    finally:
        websocket_clients.remove(client)
        if channel not in [c.channel for c in websocket_clients]:
            await unsubscribe_redis_channel(channel)
