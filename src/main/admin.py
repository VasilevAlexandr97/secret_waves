from contextlib import asynccontextmanager

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

from src.admin_panel.views import (
    AttachmentView,
    CategoryView,
    PostView,
    UserView,
)
from src.main.config import AdminConfig, PostgresConfig, load_admin_config
from src.main.providers import AuthProvider, DatabaseProvider, UserProvider


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


def setup_admin(app: FastAPI, engine: AsyncEngine) -> None:
    admin = Admin(app, engine)
    admin.add_view(UserView)
    admin.add_view(CategoryView)
    admin.add_view(PostView)
    admin.add_view(AttachmentView)


@asynccontextmanager
async def lifespan(app: FastAPI):
    current_container: AsyncContainer = app.state.dishka_container
    engine = await current_container.get(AsyncEngine)
    setup_admin(app, engine)
    yield
    await current_container.close()


def create_admin_app() -> FastAPI:
    config = load_admin_config()

    app = FastAPI(lifespan=lifespan)

    container = make_async_container(
        AdminConfigProvider(config),
        DatabaseProvider(),
        AuthProvider(),
        UserProvider(),
    )
    setup_dishka(container, app)
    return app



