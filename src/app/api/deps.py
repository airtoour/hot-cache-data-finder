from typing import Annotated

from fastapi import Depends

from src.app.core.config.cache import redis_settings
from src.app.services.cache.service import CacheService
from src.app.services.phones.service import PhonesService


def cache_service() -> CacheService:
    """Cache service dependency"""

    return CacheService(redis=redis_settings().INSTANCE)


def phones_service(cache: Annotated[CacheService, Depends(cache_service)]) -> PhonesService:
    """Phones service dependency"""

    return PhonesService(database=cache)
