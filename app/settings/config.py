from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    pythonpass: str = "app"
    api_port: int = 8000


class PostgresConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str

    @property
    def connection_uri(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    postgres: PostgresConfig

