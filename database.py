import os
import typing

import motor.motor_asyncio
from redis import asyncio as aioredis

REDIS_IP = os.getenv("REDIS_IP", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")


class RedisSingleton:
    _instance: typing.Optional[aioredis.Redis] = None

    def __new__(cls):
        raise NotImplementedError("Cannot instantiate a singleton class.")

    @classmethod
    async def get_instance(cls) -> aioredis.Redis:
        if not cls._instance:
            cls._instance = await cls._connect_to_redis()
        return cls._instance

    @staticmethod
    async def _connect_to_redis() -> aioredis.Redis:
        return await aioredis.from_url(
            f"redis://{REDIS_IP}:{REDIS_PORT}",
            username="default",
            password=REDIS_PASSWORD,
        )

    @classmethod
    async def close_redis_connection(cls):
        if cls._instance:
            await cls._instance.close()


class MongoSingleton:
    _instance: typing.Optional[motor.motor_asyncio.AsyncIOMotorClient] = None

    def __new__(cls):
        raise NotImplementedError("Cannot instantiate a singleton class.")

    @classmethod
    async def get_instance(cls) -> motor.motor_asyncio.AsyncIOMotorClient:
        if not cls._instance:
            cls._instance = await cls._connect_to_mongo()
        return cls._instance

    @staticmethod
    async def _connect_to_mongo() -> motor.motor_asyncio.AsyncIOMotorClient:
        return motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

    @classmethod
    async def close_mongo_connection(cls):
        if cls._instance:
            await cls._instance.close()
