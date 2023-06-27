from typing import Any

import pymongo
from fastapi import Depends, HTTPException

from utils.APIRouter import APIRouter
from utils.utils import get_user_object, get_mongo_instance
from .Home import Home
from .Player import Player

router = APIRouter()


@router.get("/homes", status_code=200, response_model=list[Home])
async def get_homes(
    player: Player = Depends(get_user_object),
) -> Any:
    return player.saved_homes


@router.patch("/homes", status_code=200, response_model=list[Home])
async def add_home(
    home: Home,
    player: Player = Depends(get_user_object),
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    for h in player.saved_homes:
        if h.name.lower() == home.name.lower():
            raise HTTPException(
                status_code=400, detail="You already have a home by that name."
            )
    home.name = home.name.replace(" ", "-")
    player.saved_homes.append(home)
    await player.save(instance)
    return player.saved_homes


@router.delete("/homes", status_code=200, response_model=list[Home])
async def remove_home(
    home: Home | str,
    player: Player = Depends(get_user_object),
    instance: pymongo.MongoClient = Depends(get_mongo_instance),
):
    if isinstance(home, str):
        home = home.replace(" ", "-")
        for h in player.saved_homes:
            if h.name.lower() == home.lower():
                player.saved_homes.remove(h)
                await player.save(instance)
                return player.saved_homes
        raise HTTPException(
            status_code=400, detail="You do not have a home by that name."
        )
    else:
        player.saved_homes.remove(home)
        await player.save(instance)
        return player.saved_homes
