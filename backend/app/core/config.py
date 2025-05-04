from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator, ValidationInfo

class Settings(BaseSettings):
    # Core settings
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    SQLALCHEMY_DATABASE_URI: str | None = None
    DB_ECHO: bool = False

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | PostgresDsn | None, info: ValidationInfo) -> PostgresDsn:
        if isinstance(v, (str, PostgresDsn)):
            return v
        
        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            port=info.data.get("POSTGRES_PORT"),
            path=f"{info.data.get('POSTGRES_DB') or ''}"
        ))

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()