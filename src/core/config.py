from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLITE_DSN: str = "sqlite+aiosqlite:///./database.db"
    REDIS_DSN: str = "redis://localhost:6379/0"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXP_MIN: int = 15
    JWT_REFRESH_TOKEN_EXP_DAYS: int = 7
    JWT_SECRET: str
    DEFAULT_USER_ROLE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
