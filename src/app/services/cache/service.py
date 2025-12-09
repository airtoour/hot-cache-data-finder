from typing import Any

from loguru import logger
from orjson import orjson
from redis.asyncio import Redis
from redis.exceptions import DataError
from redis.exceptions import RedisError


class CacheService:
    """Service for work App Cache"""

    def __init__(self, redis: Redis) -> None:
        self.redis: Redis = redis

        self.default_ttl: int = 86_400
        self.default_ttl_for_old_records: int = 120

        self.default_cursor_count_rows: int = 100

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

    async def update(self, key: str, data: dict[str, Any]) -> None:
        """Update Value from cache by key"""

        try:

            # Delete old value
            await self.drop(key)

            # Add new value by key
            await self.redis.set(key, orjson.dumps(data))
        except DataError as e:
            logger.error(f"Error updating {key}: {e}")
            raise e

    async def set(self, key: str, data: dict[str, Any]) -> None:
        """Set Value from cache by key"""

        try:
            return await self.redis.set(key, orjson.dumps(data), ex=self.default_ttl)
        except DataError as e:
            logger.error(f"Error setting by data: {key}: {e}")
            raise e
        except RedisError as e:
            logger.error(f"Error setting {key}: {e}")
            raise e

    async def drop_all_old_records(self) -> bool:
        """Drop all old records"""

        cursor = b"0"

        try:
            while cursor:
                cursor, keys = await self.redis.scan(cursor=cursor, count=self.default_cursor_count_rows)

                for key in keys:
                    ttl = await self.redis.ttl(key)

                    if ttl > 0 and ttl < self.default_ttl_for_old_records:
                        await self.drop(key)

                if cursor == 0 or cursor == b"0":
                    break

            return True
        except RedisError as e:
            logger.error(f"Error dropping old records: {e}")
            return False

    async def drop(self, key: str) -> None:
        """Drop Value from cache by key"""

        try:
            await self.redis.delete(key)
        except DataError as e:
            logger.error(f"Error dropping {key}: {e}")
            raise e
