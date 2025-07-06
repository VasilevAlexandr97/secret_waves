import logging

from abc import abstractmethod
from typing import Protocol

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.operators import eq

from src.core.exceptions import EntityNotFoundError
from src.core.posts.mappers import map_post_model_to_dto
from src.core.posts.models import (
    Attachment,
    AttachmentDTO,
    AttachmentId,
    Category,
    CategoryDTO,
    CategoryId,
    Post,
    PostDTO,
    PostId,
    PostStatus,
    UpdatePostDTO,
)

logger = logging.getLogger(__name__)


class CategoryRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_categories(self) -> list[CategoryDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_category_by_id(self, category_id: int) -> CategoryDTO:
        raise NotImplementedError


class AttachmentRepositoryProtocol(Protocol):
    @abstractmethod
    async def add_attachment(
        self,
        attachment_data: AttachmentDTO,
    ) -> AttachmentId:
        raise NotImplementedError


class PostRepositoryProtocol(Protocol):
    @abstractmethod
    async def add_post(self, post_data: PostDTO) -> PostId:
        raise NotImplementedError

    @abstractmethod
    async def update_post(self, update_data: UpdatePostDTO) -> PostId:
        raise NotImplementedError

    @abstractmethod
    async def get_posts_by_status(
        self,
        status: PostStatus,
        offset: int = 0,
        limit: int = 10,
    ) -> list[PostDTO]:
        raise NotImplementedError

    @abstractmethod
    async def count_posts_by_status(self, status: PostStatus) -> int:
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
            CategoryDTO(id=CategoryId(category.id), name=category.name)
            for category in categories
        ]

    async def get_category_by_id(self, category_id: int) -> CategoryDTO:
        stmt = select(Category).where(eq(Category.id, category_id))
        category = await self._session.scalar(stmt)
        if category is None:
            raise EntityNotFoundError(
                f"Category {category_id} not found",
                category_id,
            )
        return CategoryDTO(id=CategoryId(category.id), name=category.name)


class AttachmentRepository(AttachmentRepositoryProtocol):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def add_attachment(
        self,
        attachment_data: AttachmentDTO,
    ) -> AttachmentId:
        attachment_model = Attachment(
            type=attachment_data.type,
            s3_key=attachment_data.s3_key,
            file_id=attachment_data.file_id,
            post_id=attachment_data.post_id,
        )
        self._session.add(attachment_model)
        await self._session.flush()
        return AttachmentId(attachment_model.id)


class PostRepository(PostRepositoryProtocol):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def add_post(self, post_data: PostDTO) -> PostId:
        attachment_model = None
        if post_data.attachment:
            attachment_model = Attachment(
                type=post_data.attachment.type,
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
        return PostId(post_model.id)

    async def update_post(self, update_data: UpdatePostDTO) -> PostId:
        update_values = {}

        if update_data.status is not None:
            update_values["status"] = update_data.status

        if not update_values:
            return update_data.post_id

        stmt = select(Post).where(eq(Post.id, update_data.post_id))
        post = await self._session.scalar(stmt)

        stmt = (
            update(Post)
            .where(eq(Post.id, update_data.post_id))
            .values(**update_values)
        )
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise EntityNotFoundError("Post", update_data.post_id)

        await self._session.flush()
        return post.id

    async def get_posts_by_status(
        self,
        status: PostStatus,
        offset: int = 0,
        limit: int = 10,
    ) -> list[PostDTO]:
        stmt = (
            select(Post)
            .options(
                joinedload(Post.category),
                joinedload(Post.attachment),
            )
            .where(eq(Post.status, status))
            .order_by(Post.id.asc())
            .offset(offset)
            .limit(limit)
        )
        result = (await self._session.scalars(stmt)).all()
        return [map_post_model_to_dto(post) for post in result]

    async def count_posts_by_status(self, status: PostStatus) -> int:
        stmt = (
            select(func.count())
            .select_from(Post)
            .where(eq(Post.status, status))
        )
        return await self._session.scalar(stmt)
