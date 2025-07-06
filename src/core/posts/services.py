import logging
import uuid

from typing import BinaryIO

from src.core.auth.id_providers import IdProvider
from src.core.database.transaction_manager import TransactionManager
from src.core.dto import PaginationDTO
from src.core.files.dto import FileDTO
from src.core.files.exceptions import UnsupportedMimeTypeError
from src.core.files.file_manager import S3FileManager
from src.core.posts.exceptions import AttachmentCreateError, PostCreateError
from src.core.posts.models import (
    AttachmentDTO,
    AttachmentId,
    AttachmentType,
    CategoryDTO,
    PostDTO,
    PostId,
    PostStatus,
    UpdatePostDTO,
)
from src.core.posts.repositories import (
    AttachmentRepositoryProtocol,
    CategoryRepositoryProtocol,
    PostRepositoryProtocol,
)

logger = logging.getLogger(__name__)


class AttachmentService:
    def __init__(
        self,
        attachment_repository: AttachmentRepositoryProtocol,
        s3_file_manager: S3FileManager,
    ):
        self.attachment_repository = attachment_repository
        self.s3_file_manager = s3_file_manager
        self.attachment_backet = "posts/attachments"

    def get_attachment_type_by_mime(self, mime_type: str) -> AttachmentType:
        mime_to_type = {
            "audio/ogg": AttachmentType.VOICE,
        }
        attachment_type = mime_to_type.get(mime_type)
        if attachment_type is None:
            raise UnsupportedMimeTypeError(mime_type)
        return attachment_type

    def create_attachment_data(
        self,
        post_id: PostId,
        file_data: FileDTO,
    ) -> AttachmentDTO:
        s3_key = f"{self.attachment_backet}/{uuid.uuid4()}"
        mime_type = file_data.mime_type
        attachment_type = self.get_attachment_type_by_mime(mime_type)
        return AttachmentDTO(
            id=None,
            type=attachment_type,
            s3_key=s3_key,
            file_id=file_data.file_id,
            post_id=post_id,
        )

    async def add_attachment(
        self,
        attachment_data: AttachmentDTO,
    ) -> AttachmentId:
        return await self.attachment_repository.add_attachment(attachment_data)

    async def upload_attachment(
        self,
        file: BinaryIO,
        key: str,
        content_type: str | None = None,
    ) -> bool:
        return await self.s3_file_manager.upload_fileobj(
            file,
            key,
            content_type,
        )

    async def create_attachment(
        self,
        post_id: PostId,
        file_data: FileDTO,
    ) -> AttachmentId:
        try:
            attachment_data = self.create_attachment_data(post_id, file_data)
            attachment_id = await self.add_attachment(attachment_data)
            await self.upload_attachment(
                file_data.file,
                attachment_data.s3_key,
                file_data.mime_type,
            )
        except UnsupportedMimeTypeError:
            logger.exception(
                "Attachment create error. "
                f"Unsupported mime type: {file_data.mime_type}",
            )
            raise AttachmentCreateError
        else:
            return attachment_id

    async def get_attachment_url(self, key: str) -> str:
        return await self.s3_file_manager.generate_presigned_url(key)

# TODO: transaction_manager и s3_file_manager - Protocol
class PostService:
    def __init__(
        self,
        category_repository: CategoryRepositoryProtocol,
        post_repository: PostRepositoryProtocol,
        transaction_manager: TransactionManager,
        attachment_service: AttachmentService,
    ):
        self.category_repository = category_repository
        self.post_repository = post_repository
        self.transaction_manager = transaction_manager
        self.attachment_service = attachment_service

    async def create_post(
        self,
        id_provider: IdProvider | None,
        post_data: PostDTO,
        file_data: FileDTO | None = None,
    ) -> int:
        logger.info(
            f"Create post with data: id_provider: {id_provider}, "
            f" post data: {post_data}, file_data: {file_data}",
        )
        try:
            if id_provider is not None:
                user_id = await id_provider.get_current_user_id()
                post_data.user_id = user_id
            else:
                post_data.user_id = None

            async with self.transaction_manager:
                post_id = await self.post_repository.add_post(post_data)
                if file_data:
                    await self.attachment_service.create_attachment(
                        post_id,
                        file_data,
                    )
                return post_id
        except AttachmentCreateError:
            logger.exception("Post create error. Attachment create error")
            raise PostCreateError
        except Exception:
            logger.exception("Post create error")
            raise PostCreateError

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

    async def get_posts_for_moderation(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> PaginationDTO[PostDTO]:
        posts = await self.post_repository.get_posts_by_status(
            PostStatus.PENDING,
            limit=limit,
            offset=offset,
        )
        for post in posts:
            if post.attachment:
                url = await self.attachment_service.get_attachment_url(
                    post.attachment.s3_key,
                )
                logger.debug(f"url: {url}")
                post.attachment.url = url
        count = await self.post_repository.count_posts_by_status(
            PostStatus.PENDING,
        )
        return PaginationDTO(
            items=posts,
            count=count,
            offset=offset,
            limit=limit,
        )
