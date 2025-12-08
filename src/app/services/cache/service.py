from typing import Any

from loguru import logger
from orjson import orjson
from redis.asyncio import Redis
from redis.exceptions import DataError


class CacheService:
    """Service for work App Cache"""

    def __init__(self, redis: Redis) -> None:
        self.redis: Redis = redis

        self.default_ttl: int = 86_400

    async def get(self, key: str) -> Any:
        """Get Value from cache by key"""

        try:
            return await self.redis.get(key)
        except DataError as e:
            logger.error(f"Error getting {key}: {e}")
            raise e

    async def update_ttl(self, key: str, ttl: int) -> None:
        """Update TTL in cache by key"""

        try:
            await self.redis.expire(key, ttl)
        except DataError as e:
            logger.error(f"Error updating {key}: {e}")
            raise e

    async def update(self, key: str, data: Any) -> None:
        """Update Value from cache by key"""

        try:

            # Delete old value
            await self.redis.delete(key)

            # Add new value by key
            await self.redis.set(key, orjson.dumps(data))
        except DataError as e:
            logger.error(f"Error updating {key}: {e}")
            raise e

    async def set(self, key: str, data: Any) -> None:
        """Set Value from cache by key"""

        try:
            return await self.redis.set(key, orjson.dumps(data), ex=self.default_ttl)
        except DataError as e:
            logger.error(f"Error setting {key}: {e}")
            raise e
