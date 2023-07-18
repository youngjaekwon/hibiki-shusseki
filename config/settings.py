import secrets
from typing import Any

from pydantic import AnyHttpUrl, validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    authjwt_secret_key: str = secrets.token_urlsafe(32)
    authjwt_access_token_expires: int = 60 * 60 * 12 # 12 hours
    authjwt_refresh_token_expires: int = 60 * 60 * 24 * 8 # 8 days
    SERVER_NAME: str = "localhost:8000"
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> str | list[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    SQLALCHEMY_DATABASE_URI: str
    # POSTGRES_SERVER: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    # POSTGRES_SCHEME: str
    # SQLALCHEMY_DATABASE_URI: str

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme=values.get("POSTGRES_SCHEME"),
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_prefix="",
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
