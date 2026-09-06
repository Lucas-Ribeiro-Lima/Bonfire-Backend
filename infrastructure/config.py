from typing import Any

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from infrastructure.exceptions import MissingRequiredEnvError


class Config(BaseSettings):
    """Application configuration loaded from environment variables and optional .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    DB_DRIVER: str = Field(default="mysql", description="Database driver name")
    DB_HOST: str = Field(default="bonfire-db", description="Database host")
    DB_PORT: int | str = Field(default=3306, description="Database port")
    DB_NAME: str = Field(default="bonfire", description="Database name")
    DB_USER: str = Field(default="bonfire", description="Database user")
    DB_PASSWORD: str = Field(..., description="Database password")

    # Auth (Keycloak)
    KEYCLOAK_ISSUER: str = Field(
        default="http://keycloak:8080", description="Keycloak issuer URL"
    )
    KEYCLOAK_CLIENT_ID: str = Field(default="bonfire", description="Keycloak client ID")
    KEYCLOAK_CLIENT_SECRET: str = Field(..., description="Keycloak client secret")
    KEYCLOAK_REALM_NAME: str = Field(..., description="Keycloak realm name")

    def __init__(self, **values: Any) -> None:
        super().__init__(**values)

    def __getitem__(self, item: str) -> Any:
        try:
            return getattr(self, item)
        except AttributeError:
            raise KeyError(f"Configuration variable '{item}' not found.")

    def __setitem__(self, key: str, value: Any) -> None:
        if not hasattr(self, key):
            raise KeyError(f"Cannot set or modify variable '{key}'.")
        setattr(self, key, value)


def load_config() -> Config:
    """Load configuration, mapping missing required environment variables to MissingRequiredEnvError."""
    try:
        return Config()
    except ValidationError as exc:
        for err in exc.errors():
            if err.get("type") == "missing":
                missing_field = str(err["loc"][0])
                raise MissingRequiredEnvError(missing_field) from exc
        raise


config = load_config()
