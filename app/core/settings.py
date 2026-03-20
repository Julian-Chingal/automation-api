from pydantic import Field, computed_field, field_validator, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from .exceptions import ConfigurationError
from typing import Literal, Dict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
        case_sensitive=True,
        env_ignore_empty=True
    )

    # Aplication
    APPLICATION_TITLE:str
    APPLICATION_SUMMARY:str
    APPLICATION_DESCRIPTION:str
    APPLICATION_VERSION:str
    PORT: int

    # Environment
    APP_ENV:Literal["DEV", "QA", "PROD"]

    # Cors
    CORS_ORIGINS: list
    ALLOWED_HOST: list

    # Security
    SECURITY_API_KEY_HEADER: str
    SECURITY_API_KEY_HEADER_DESCRIPTION: str
    SECURITY_SCHEME_NAME: str
    SECURITY_DEFAULT_API_KEY: SecretStr  

    # Database
    DATABASES: Dict[str, str] = Field(default_factory=dict)

    @computed_field
    @property
    def ENVIRONMENT_DEBUG(self) -> bool:
        return self.APP_ENV == "DEV"
    
    @field_validator("DATABASES")
    @classmethod
    def validate_databases(cls, databases: Dict[str, str]):

        if not databases:
            raise ConfigurationError("At least one database must be configured")

        for alias, uri in databases.items():

            if not alias.isidentifier():
                raise ValueError(
                    f"Invalid database alias '{alias}'"
                )

            if not uri.startswith(
                ("postgresql://", "mysql+pymysql://")
            ):
                raise ConfigurationError(
                    f"Invalid URI scheme for database '{alias}'"
                )

        return databases
    
settings = Settings()