from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


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


class AuthConfig(BaseModel):
    algorithm: str
    private_key_pass: Path = BASE_DIR / "private_key.pem"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    postgres: PostgresConfig
    auth: AuthConfig
