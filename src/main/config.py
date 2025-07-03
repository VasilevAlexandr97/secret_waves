from pathlib import Path

import yaml

from pydantic import Field, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PATH = Path(__file__).resolve().parent.parent.parent

def read_yaml(path: Path) -> dict:
    with Path.open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


class PostgresConfig(BaseSettings):
    host: str
    port: int
    user: str
    password: SecretStr
    database: str

    @property
    def dsn_psycopg2(self) -> str:
        return f"postgresql://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"

    @property
    def dsn_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"


class RedisConfig(BaseSettings):
    host: str
    port: str
    password: SecretStr

    @property
    def dsn(self) -> str:
        return f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}"


class AdminConfig(BaseSettings):
    postgres: PostgresConfig

    templates_dir_path: Path = BASE_PATH / "src/admin_panel/templates"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )


class TgBotConfig(BaseSettings):
    base_path: Path = Field(
        default=Path(__file__).parent.parent,
    )
    messages: dict[str, str] = Field(default_factory=dict)

    postgres: PostgresConfig
    redis: RedisConfig

    telegram_token: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    @field_validator("messages", mode="after")
    @classmethod
    def _load_messages_yaml(
        cls,
        v: dict,
        info: ValidationInfo,
    ) -> dict[str, str]:
        base_path = info.data["base_path"]
        yaml_path = base_path / "telegram_bot/data/messages.yaml"
        if not yaml_path.exists():
            raise FileNotFoundError(f"messages.yaml not found in {yaml_path}")
        return read_yaml(yaml_path)


def load_admin_config() -> AdminConfig:
    return AdminConfig()


def load_tgbot_config() -> TgBotConfig:
    return TgBotConfig()
