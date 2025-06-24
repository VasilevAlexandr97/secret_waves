from src.core.posts.models import CategoryDTO
from src.core.posts.repositories import CategoryRepositoryProtocol


class PostServices:
    def __init__(self, category_repository: CategoryRepositoryProtocol):
        self.category_repository = category_repository

    async def get_categories(self) -> list[CategoryDTO]:
        return await self.category_repository.get_categories()
