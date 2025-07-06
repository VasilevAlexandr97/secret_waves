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
from src.core.files.file_manager import S3FileManager
from src.core.posts.repositories import (
    AttachmentRepository,
    AttachmentRepositoryProtocol,
    CategoryRepository,
    CategoryRepositoryProtocol,
    PostRepository,
    PostRepositoryProtocol,
)
from src.core.posts.services import AttachmentService, PostService
from src.core.users.repositories import UserRepository, UserRepositoryProtocol
from src.main.config import PostgresConfig, S3Config


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


class S3Provider(Provider):
    @provide(scope=Scope.APP)
    def get_s3_file_manager(self, config: S3Config) -> S3FileManager:
        return S3FileManager(settings=config)

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

    attachment_repository = provide(
        AttachmentRepository,
        scope=Scope.REQUEST,
    )
    attachment_repository_protocol = alias(
        source=AttachmentRepository,
        provides=AttachmentRepositoryProtocol,
    )
    attachment_service = provide(
        AttachmentService,
        scope=Scope.REQUEST,
    )
    post_repository = provide(
        PostRepository,
        scope=Scope.REQUEST,
    )
    post_repository_protocol = alias(
        source=PostRepository,
        provides=PostRepositoryProtocol,
    )

    post_services = provide(
        PostService,
        scope=Scope.REQUEST,
    )
