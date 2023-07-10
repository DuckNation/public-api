from fastapi import APIRouter

from .motd import router as motd_router

router = APIRouter(prefix="/motd")
router.include_router(motd_router)
