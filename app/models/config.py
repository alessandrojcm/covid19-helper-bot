from pydantic import BaseSettings, AnyHttpUrl
from pydantic.dataclasses import dataclass
from pydantic.types import SecretStr

from app.models.environments import Environments
from app.models.logging_levels import LoggingLevels


@dataclass()
class Config(BaseSettings):
    API_PREFIX: str = "/api"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    TESTING: bool = False
    PROJECT_NAME: str = "COVID19 Helper Bot"
    LOGGING_LEVEL: LoggingLevels = LoggingLevels.INFO
    ENVIRONMENT: Environments = Environments.DEV
    FAUNA_DB_HOST: AnyHttpUrl = "http://localhost:8443"
    FAUNA_SERVER_KEY: SecretStr = "your_server_key_here"
    FAUNA_DB_PORT: int = 8443

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __post_init_post_parse__(self):
        self.LOGGING_LEVEL = LoggingLevels.DEBUG if self.DEBUG else LoggingLevels.INFO
