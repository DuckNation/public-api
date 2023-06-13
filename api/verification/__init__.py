from fastapi import APIRouter

from .create_pin import router as create_pin_router
from .unverify import router as unverify_router
from .verify import router as verify_router

router = APIRouter(prefix="/verification")
router.include_router(verify_router)
router.include_router(unverify_router)
router.include_router(create_pin_router)
