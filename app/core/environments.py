from enum import Enum


class Environments(str, Enum):
    DEV = "dev"
    STAGING = "staging"
    PRODUCTION = "production"
