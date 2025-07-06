import logging

from src.core.posts.models import (
    Attachment,
    AttachmentDTO,
    AttachmentId,
    AttachmentType,
    Category,
    CategoryDTO,
    CategoryId,
    Post,
    PostDTO,
    PostId,
    PostStatus,
)

logger = logging.getLogger(__name__)


def map_category_model_to_dto(category: Category) -> CategoryDTO:
    return CategoryDTO(
        id=CategoryId(category.id),
        name=category.name,
    )


def map_attachment_model_to_dto(attachment: Attachment) -> AttachmentDTO:
    return AttachmentDTO(
        id=AttachmentId(attachment.id),
        type=AttachmentType(attachment.type),
        s3_key=attachment.s3_key,
        file_id=attachment.file_id,
        post_id=attachment.post_id,
    )


def map_post_model_to_dto(post: Post) -> PostDTO:
    attachment = None
    category = None
    logger.debug(f"post_category: {post.category}")
    if post.category:
        category = map_category_model_to_dto(post.category)
    logger.debug(f"post_attachment: {post.attachment}")
    if post.attachment:
        attachment = map_attachment_model_to_dto(post.attachment)
        logger.debug(f"{type(attachment)}")
    return PostDTO(
        id=PostId(post.id),
        content=post.content,
        category_id=post.category_id,
        category=category,
        attachment=attachment,
        user_id=post.user_id,
        status=PostStatus(post.status),
    )
