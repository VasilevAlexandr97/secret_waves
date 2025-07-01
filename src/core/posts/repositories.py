from abc import abstractmethod
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import eq

from src.core.posts.models import (
    Attachment,
    Category,
    CategoryDTO,
    Post,
    PostDTO,
)


class CategoryRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_categories(self) -> list[CategoryDTO]:
        raise NotImplementedError


class CategoryRepository(CategoryRepositoryProtocol):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def get_categories(self) -> list[CategoryDTO]:
        stmt = select(Category).order_by(Category.id.asc())
        categories = await self._session.scalars(stmt)
        return [
            CategoryDTO(id=category.id, name=category.name)
            for category in categories
        ]

    async def get_category_by_id(self, category_id: int) -> CategoryDTO:
        stmt = select(Category).where(eq(Category.id, category_id))
        category = await self._session.scalar(stmt)
        return CategoryDTO(id=category.id, name=category.name)


# None: описать протокол
class PostRepositoryProtocol(Protocol):
    pass


class PostRepository(PostRepositoryProtocol):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def add_post(self, post_data: PostDTO) -> int:
        attachment_model = None
        if post_data.attachment:
            attachment_model = Attachment(
                attachment_type=post_data.attachment.attachment_type,
                file_id=post_data.attachment.file_id,
            )
        post_model = Post(
            content=post_data.content,
            category_id=post_data.category_id,
            attachment=attachment_model,
            user_id=post_data.user_id,
        )
        self._session.add(post_model)
        await self._session.flush()
        return post_model.id
