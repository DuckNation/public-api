import uuid

import pymongo
from fastapi import Request

from database import MongoSingleton


def get_param_from_request(param_name: str, request: Request):
    return request.query_params.get(param_name, "")


async def get_mongo_instance() -> pymongo.MongoClient:
    return await MongoSingleton.get_instance()


def format_uuid(uuid_str: str) -> str:
    return str(uuid.UUID(uuid_str)).upper()


def format_uuid_args(*args) -> list | str:
    if len(args) == 1:
        return format_uuid(args[0])
    return [format_uuid(arg) for arg in args]
