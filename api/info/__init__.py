from fastapi import APIRouter

from .get import router as get_router
from .fly import router as fly_router
from .home_related import router as home_router

router = APIRouter(prefix="/info")
router.include_router(get_router)
router.include_router(fly_router)
router.include_router(home_router)
