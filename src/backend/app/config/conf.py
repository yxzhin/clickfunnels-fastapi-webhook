# This file is meant to be imported at the start of the app.
# It checks if the required environment variables are loaded,
# as well as init a class that's used to store environment variables

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # required
    APP_NAME: str = Field(min_length=1)
    APP_DESCRIPTION: str = Field(min_length=1)
    APP_VERSION: str = Field(min_length=1)

    CLICKFUNNELS_SUBDOMAIN: str = Field(min_length=1)
    CLICKFUNNELS_WORKSPACE_ID: int = Field(min_length=1)
    CLICKFUNNELS_API_TOKEN: str = Field(min_length=1)
    CLICKFUNNELS_WEBHOOK_SECRET: str = Field(min_length=1)

    REDIS_URL: str = Field(min_length=1)

    # optional
    TIME_ZONE: str = "America/Los_Angeles"
    EVENT_TTL_SECONDS: int = 86400
    ENABLE_API_DOCS: bool = True
    LOG_RAW_PAYLOAD: bool = False  # log incoming payloads (avoid in prod unless needed)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_config() -> Config:
    return Config()  # type: ignore
