import logging

from contextlib import asynccontextmanager
from pathlib import Path

from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
    provide,
)
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine

from src.admin_panel.views.posts import (
    AttachmentView,
    CategoryView,
    ModerationPostView,
    PostView,
    router as admin_posts_router,
)
from src.admin_panel.views.users import UserView
from src.main.config import (
    AdminConfig,
    PostgresConfig,
    S3Config,
    load_admin_config,
)
from src.main.providers import (
    AuthProvider,
    DatabaseProvider,
    PostProvider,
    S3Provider,
    UserProvider,
)

logger = logging.getLogger(__name__)


class AdminConfigProvider(Provider):
    def __init__(self, config: AdminConfig):
        super().__init__()
        self.config = config

    @provide(scope=Scope.APP)
    def get_config(self) -> AdminConfig:
        return self.config

    @provide(scope=Scope.APP)
    def get_postgres_config(self) -> PostgresConfig:
        return self.config.postgres

    @provide(scope=Scope.APP)
    def s3_config(self) -> S3Config:
        return self.config.s3


def setup_admin_views(
    app: FastAPI,
    engine: AsyncEngine,
    templates_dir_path: Path,
) -> None:
    admin = Admin(
        app,
        engine,
        templates_dir=str(templates_dir_path),
        debug=True,
    )
    admin.add_view(UserView)
    admin.add_view(CategoryView)
    admin.add_view(PostView)
    admin.add_view(AttachmentView)
    admin.add_view(ModerationPostView)


def setup_admin_routes(app: FastAPI) -> None:
    app.include_router(admin_posts_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Admin App Lifespan Started")
    current_container: AsyncContainer = app.state.dishka_container
    engine = await current_container.get(AsyncEngine)
    admin_config = await current_container.get(AdminConfig)
    setup_admin_views(app, engine, admin_config.templates_dir_path)
    yield
    await current_container.close()
    logger.info("Admin App Lifespan Finished")


def create_admin_app() -> FastAPI:
    config = load_admin_config()
    logging.basicConfig(
        level=logging.INFO if not config.debug else logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    )
    logger.info("Admin App Started")
    logger.info(f"Debug Mode: {config.debug}")

    app = FastAPI(lifespan=lifespan, debug=config.debug)
    setup_admin_routes(app)
    container = make_async_container(
        AdminConfigProvider(config),
        DatabaseProvider(),
        AuthProvider(),
        UserProvider(),
        PostProvider(),
        S3Provider(),
    )
    setup_dishka(container, app)
    return app
