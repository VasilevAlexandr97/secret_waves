from src.core.auth.id_providers import IdProvider
from src.core.database.transaction_manager import TransactionManager
from src.core.posts.models import CategoryDTO, PostDTO
from src.core.posts.repositories import (
    CategoryRepositoryProtocol,
    PostRepositoryProtocol,
)


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

    async def get_categories(self) -> list[CategoryDTO]:
        return await self.category_repository.get_categories()

    async def get_category_by_id(self, category_id: int) -> CategoryDTO:
        return await self.category_repository.get_category_by_id(category_id)

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
