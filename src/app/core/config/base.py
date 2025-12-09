from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Base settings for project"""

    API_V1_PREFIX: str = "/api/v1"


@lru_cache()
def settings() -> Settings:
    return Settings()
