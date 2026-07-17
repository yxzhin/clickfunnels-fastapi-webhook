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

    CADDY_DOMAIN: str = Field(min_length=1)
    CADDY_EMAIL: str = Field(min_length=1)

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

    @property
    def api_base_url(self) -> str:
        return f"https://{self.CLICKFUNNELS_SUBDOMAIN}.myclickfunnels.com/api/v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        str_strip_whitespace=True,
        case_sensitive=False,
    )


@lru_cache
def get_config() -> Config:
    return Config()  # type: ignore
