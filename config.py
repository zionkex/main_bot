from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str
    echo: bool = False
    max_overflow: int = 10
    @property
    def postgres_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:5435/{self.postgres_db}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='APP_CONFIG__'
    )
    db: DatabaseConfig
    TOKEN :str


settings = Settings()