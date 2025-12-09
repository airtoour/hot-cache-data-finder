from fastapi import APIRouter

from src.app.api.v1.phones import router as phones_router
from src.app.core.config.base import settings

api_router = APIRouter(prefix=settings().API_V1_PREFIX)

api_router.include_router(phones_router)
