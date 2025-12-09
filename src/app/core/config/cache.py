from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from redis.asyncio import Redis


class CacheSettings(BaseSettings):
    """Cache settings"""

    BASE_DIR: Path = Path(__file__).resolve().parents[4]

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_ignore_empty=True, extra="ignore", env_prefix="REDIS_"
    )

    HOST: str = Field(default="localhost")
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
