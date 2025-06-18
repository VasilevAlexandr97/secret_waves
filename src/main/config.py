from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


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


class AdminConfig(BaseSettings):
    postgres: PostgresConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )


class TgBotConfig(BaseSettings):
    postgres: PostgresConfig
    telegram_token: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )


def load_admin_config() -> AdminConfig:
    return AdminConfig()


def load_tgbot_config() -> TgBotConfig:
    return TgBotConfig()
