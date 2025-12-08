from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings
from redis.asyncio import Redis


class CacheSettings(BaseSettings):
    """Cache settings"""

    HOST: str = Field(default="redis")
    PORT: int = Field(default=6379)
    DB: int = Field(default=0)

    # For deployment needed
    # PASSWORD: str = Field(default="password")

    @property
    def INSTANCE(self) -> Redis:  # noqa
        return Redis(
            host=self.HOST,
            port=self.PORT,
            db=self.DB,
            # password=self.PASSWORD
        )


@lru_cache()
def redis_settings() -> CacheSettings:
    return CacheSettings()
