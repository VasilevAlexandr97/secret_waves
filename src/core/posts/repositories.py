from abc import abstractmethod
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.posts.models import Category, CategoryDTO


class CategoryRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_categories(self) -> list[CategoryDTO]:
        raise NotImplementedError


class CategoryRepository(CategoryRepositoryProtocol):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_categories(self) -> list[CategoryDTO]:
        stmt = select(Category).order_by(Category.id.asc())
        categories = await self.session.scalars(stmt)
        return [
            CategoryDTO(id=category.id, name=category.name)
            for category in categories
        ]
