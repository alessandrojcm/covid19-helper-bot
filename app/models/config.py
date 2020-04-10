from typing import Optional

from pydantic import BaseSettings, AnyHttpUrl, validator
from pydantic.dataclasses import dataclass
from pydantic.types import SecretStr

from app.models.environments import Environments
from app.models.logging_levels import LoggingLevels


@dataclass()
class Config(BaseSettings):
    API_PREFIX: str = "/api"
    AUTOPILOT_ENDPOINT_PREFIX: str = "/autopilot"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    TESTING: bool = False
    PROJECT_NAME: str = "COVID19 Helper Bot"
    LOGGING_LEVEL: LoggingLevels = LoggingLevels.INFO
    ENVIRONMENT: Environments = Environments.DEV
    FAUNA_DB_URL: AnyHttpUrl = "http://localhost:8443"
    FAUNA_SERVER_KEY: SecretStr = "your_server_key_here"
    TWILIO_ENDPOINT: AnyHttpUrl = "http://localhost:5000"
    TWILIO_AUTH_TOKEN: Optional[str]
    SENTRY_DSN: Optional[AnyHttpUrl]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __post_init_post_parse__(self):
        self.LOGGING_LEVEL = LoggingLevels.DEBUG if self.DEBUG else LoggingLevels.INFO

    @validator("TWILIO_AUTH_TOKEN")
    def check_for_twilio_token(cls, v, values):
        if (
            "ENVIRONMENT" in values
            and values["ENVIRONMENT"] != Environments.DEV
            and not v
        ):
            raise RuntimeError("TWILIO_AUTH_TOKEN must be set")
        return v
