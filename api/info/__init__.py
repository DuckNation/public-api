from fastapi import APIRouter

from .get import router as get_router

router = APIRouter(prefix="/info")
router.include_router(get_router)
