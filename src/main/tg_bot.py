from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.aiogram import setup_dishka

from src.main.config import PostgresConfig, TgBotConfig, load_tgbot_config
from src.main.providers import (
    AuthProvider,
    DatabaseProvider,
    PostProvider,
    UserProvider,
)
from src.telegram_bot.handlers.private.start import start_router
from src.telegram_bot.middlewares.id_provider import IdProviderMiddleware
from src.telegram_bot.services.message_service import MessageService


class TgBotConfigProvider(Provider):
    def __init__(self, config: TgBotConfig):
        super().__init__()
        self.config = config

    @provide(scope=Scope.APP)
    def get_config(self) -> TgBotConfig:
        return self.config

    @provide(scope=Scope.APP)
    def get_postgres_config(self) -> PostgresConfig:
        return self.config.postgres

    @provide(scope=Scope.APP)
    def get_message_service(self) -> MessageService:
        return MessageService(self.config.messages)


def create_tgbot_app() -> tuple[Bot, Dispatcher]:
    config = load_tgbot_config()

    bot = Bot(
        token=config.telegram_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Include middlewares
    dp.message.middleware(IdProviderMiddleware())

    # Include handlers
    dp.include_router(start_router)

    container = make_async_container(
        TgBotConfigProvider(config),
        DatabaseProvider(),
        AuthProvider(),
        UserProvider(),
        PostProvider(),
    )
    setup_dishka(container, dp)
    return bot, dp
