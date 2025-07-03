import logging

from src.core.auth.id_providers import IdProvider
from src.core.database.transaction_manager import TransactionManager
from src.core.dto import PaginationDTO
from src.core.posts.models import (
    CategoryDTO,
    PostDTO,
    PostId,
    PostStatus,
    UpdatePostDTO,
)
from src.core.posts.repositories import (
    CategoryRepositoryProtocol,
    PostRepositoryProtocol,
)

logger = logging.getLogger(__name__)


class PostService:
    def __init__(
        self,
        category_repository: CategoryRepositoryProtocol,
        post_repository: PostRepositoryProtocol,
        transaction_manager: TransactionManager,
    ):
        self.category_repository = category_repository
        self.post_repository = post_repository
        self.transaction_manager = transaction_manager

    async def create_post(
        self,
        post_data: PostDTO,
        id_provider: IdProvider | None,
    ) -> int:
        if id_provider is not None:
            user_id = await id_provider.get_current_user_id()
            post_data.user_id = user_id
        else:
            post_data.user_id = None

        async with self.transaction_manager:
            return await self.post_repository.add_post(post_data)

    async def approve_post(self, post_id: PostId):
        async with self.transaction_manager:
            update_data = UpdatePostDTO(
                post_id=post_id,
                status=PostStatus.APPROVED,
            )
            await self.post_repository.update_post(update_data)

    async def reject_post(self, post_id: PostId):
        async with self.transaction_manager:
            update_data = UpdatePostDTO(
                post_id=post_id,
                status=PostStatus.REJECTED,
            )
            await self.post_repository.update_post(update_data)

    async def get_categories(self) -> list[CategoryDTO]:
        return await self.category_repository.get_categories()

    async def get_category_by_id(self, category_id: int) -> CategoryDTO:
        return await self.category_repository.get_category_by_id(category_id)

    # TODO(я): Написать Protocol
    async def get_pending_posts(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> PaginationDTO[PostDTO]:
        posts = await self.post_repository.get_posts_by_status(
            PostStatus.PENDING,
            limit=limit,
            offset=offset,
        )
        count = await self.post_repository.count_posts_by_status(
            PostStatus.PENDING,
        )
        return PaginationDTO(
            items=posts,
            count=count,
            offset=offset,
            limit=limit,
        )
