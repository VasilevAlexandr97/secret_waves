from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.aiogram import setup_dishka

from src.main.config import (
    PostgresConfig,
    S3Config,
    TgBotConfig,
    load_tgbot_config,
)
from src.main.providers import (
    AuthProvider,
    DatabaseProvider,
    PostProvider,
    S3Provider,
    UserProvider,
)
from src.telegram_bot.dialogs.main.dialogs import main_dialog
from src.telegram_bot.dialogs.posts.dialogs import create_post_dialog
from src.telegram_bot.handlers.private.posts import posts_router
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
    def get_s3_config(self) -> S3Config:
        return self.config.s3

    @provide(scope=Scope.APP)
    def get_message_service(self) -> MessageService:
        return MessageService(self.config.messages)


def setup_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(posts_router)
    dp.include_router(main_dialog)
    dp.include_router(create_post_dialog)


def create_tgbot_app() -> tuple[Bot, Dispatcher]:
    config = load_tgbot_config()

    storage = RedisStorage.from_url(config.redis.dsn)
    storage.key_builder = DefaultKeyBuilder(with_destiny=True)

    bot = Bot(
        token=config.telegram_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    # Include middlewares
    dp.message.middleware(IdProviderMiddleware())
    dp.callback_query.middleware(IdProviderMiddleware())

    setup_handlers(dp)

    container = make_async_container(
        TgBotConfigProvider(config),
        DatabaseProvider(),
        AuthProvider(),
        UserProvider(),
        PostProvider(),
        S3Provider(),
    )
    setup_dishka(container, dp)
    setup_dialogs(dp)
    return bot, dp
