from pydantic import BaseSettings
from pydantic.dataclasses import dataclass

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __post_init_post_parse__(self):
        self.LOGGING_LEVEL = LoggingLevels.DEBUG if self.DEBUG else LoggingLevels.INFO
