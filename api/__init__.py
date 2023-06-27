from fastapi import Depends

from api.auth.auth import verify_http_api_key, verify_ws_api_key
from api.chats import router as chat_router
from api.info import router as info_router
from api.verification import router as verification_router
from api.wss import router as wss_router
from utils.APIRouter import APIRouter
from .verification import verify, create_pin, unverify

router = APIRouter(prefix="/api", tags=["Protected API"])

router.include_router(verification_router, dependencies=[Depends(verify_http_api_key)])
router.include_router(wss_router, dependencies=[Depends(verify_ws_api_key)])
router.include_router(chat_router, dependencies=[Depends(verify_http_api_key)])
router.include_router(info_router, dependencies=[Depends(verify_http_api_key)])
