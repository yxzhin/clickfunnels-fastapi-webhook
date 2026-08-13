# This file is meant to be imported at the start of the app.
# It checks if the required environment variables are loaded,
# as well as init a class that's used to store environment variables

from functools import lru_cache
from typing import Self

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class Config(BaseSettings):
    # required
    APP_NAME: str = Field(min_length=1)
    APP_DESCRIPTION: str = Field(min_length=1)
    APP_VERSION: str = Field(min_length=1)

    DB_HOST: str = Field(min_length=1)
    DB_PORT: str = Field(min_length=1)
    DB_USER: str = Field(min_length=1)
    DB_PASS: str = Field(min_length=1)
    DB_NAME: str = Field(min_length=1)

    CLICKFUNNELS_SUBDOMAIN: str = Field(min_length=1)
    CLICKFUNNELS_WORKSPACE_ID: str = Field(min_length=1)
    CLICKFUNNELS_API_TOKEN: str = Field(min_length=1)
    CLICKFUNNELS_WEBHOOK_SECRET: str = Field(min_length=1)

    TWILIO_ACCOUNT_SID: str = Field(min_length=1)
    TWILIO_AUTH_TOKEN: str = Field(min_length=1)
    TWILIO_FROM_NUMBER: str = Field(min_length=1)

    TWILIO_TEST_ACCOUNT_SID: str = Field(default="optional")
    TWILIO_TEST_AUTH_TOKEN: str = Field(default="optional")
    TWILIO_TEST_PHONE_NUMBER: str = Field(default="+15005550006")

    REDIS_URL: str = Field(min_length=1)

    # log incoming payloads (avoid in prod unless needed)
    LOG_RAW_PAYLOAD: bool = Field(default=False)

    REGISTRATION_TODAY_LA_PAGE_NAME: str = Field(min_length=1)
    REGISTRATION_TODAY_AU_PAGE_NAME: str = Field(min_length=1)
    REGISTRATION_TOMORROW_LA_PAGE_NAME: str = Field(min_length=1)
    REGISTRATION_TOMORROW_AU_PAGE_NAME: str = Field(min_length=1)
    LIVE_ONLINE_WEBINAR_PAGE_NAME: str = Field(min_length=1)

    DISCORD_WEBHOOK_URL: str = Field(default="optional")

    @property
    def api_base_url(self: Self) -> str:
        return f"https://{self.CLICKFUNNELS_SUBDOMAIN}.myclickfunnels.com/api/v2/workspaces/{self.CLICKFUNNELS_WORKSPACE_ID}"

    @property
    def database_url(self: Self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        str_strip_whitespace=True,
        case_sensitive=False,
    )

    @classmethod
    def settings_customise_sources(
        cls: type[Self],
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, env_settings, dotenv_settings


@lru_cache
def get_config() -> Config:
    return Config()  # type: ignore
