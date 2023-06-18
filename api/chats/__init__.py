from fastapi import APIRouter

from .block import router as block_router
from .change_password import router as password_router
from .create import router as create_router
from .get_chats_for import router as get_router
from .join import router as join_router
from .leave import router as leave_router
from .unblock import router as unblock_router

router = APIRouter(prefix="/chats")
router.include_router(create_router)
router.include_router(join_router)
router.include_router(leave_router)
router.include_router(password_router)
router.include_router(block_router)
router.include_router(unblock_router)
router.include_router(get_router)
