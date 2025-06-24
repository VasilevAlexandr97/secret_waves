from collections.abc import AsyncIterable

from dishka import (
    Provider,
    Scope,
    alias,
    provide,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.auth.services import AuthService
from src.core.database.transaction_manager import (
    TransactionManager,
    TransactionManagerInterface,
)
from src.core.posts.repositories import CategoryRepository, CategoryRepositoryProtocol
from src.core.posts.services import PostServices
from src.core.users.repositories import UserRepository, UserRepositoryProtocol
from src.main.config import PostgresConfig


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, postgres_config: PostgresConfig) -> AsyncEngine:
        return create_async_engine(postgres_config.dsn_asyncpg)

    @provide(scope=Scope.APP)
    def get_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    transaction_manager = provide(
        TransactionManager,
        scope=Scope.REQUEST,
    )
    transaction_manager_interface = alias(
        source=TransactionManager,
        provides=TransactionManagerInterface,
    )


class AuthProvider(Provider):
    auth_service = provide(
        AuthService,
        scope=Scope.REQUEST,
    )


class UserProvider(Provider):
    user_repository = provide(
        UserRepository,
        scope=Scope.REQUEST,
    )
    user_repository_protocol = alias(
        source=UserRepository,
        provides=UserRepositoryProtocol,
    )


class PostProvider(Provider):
    category_repository = provide(
        CategoryRepository,
        scope=Scope.REQUEST,
    )
    category_repository_protocol = alias(
        source=CategoryRepository,
        provides=CategoryRepositoryProtocol,
    )

    post_services = provide(
        PostServices,
        scope=Scope.REQUEST,
    )
