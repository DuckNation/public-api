import json
import typing

import motor.motor_asyncio
from redis import asyncio as aioredis

config = json.load(open("config.json"))


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
            f"redis://{config['redis-ip']}:{config['redis-port']}",
            username="default",
            password=config["redis-password"]
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
        return motor.motor_asyncio.AsyncIOMotorClient(config["mongo-uri"])

    @classmethod
    async def close_mongo_connection(cls):
        if cls._instance:
            await cls._instance.close()
