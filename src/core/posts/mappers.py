from src.core.posts.models import (
    Attachment,
    AttachmentDTO,
    AttachmentType,
    Post,
    PostDTO,
    PostStatus,
)

import logging

logger = logging.getLogger(__name__)
def map_attachment_model_to_dto(attachment: Attachment) -> AttachmentDTO:
    return AttachmentDTO(
        id=attachment.id,
        attachment_type=AttachmentType(attachment.attachment_type),
        file_id=attachment.file_id,
        post_id=attachment.post_id,
    )


def map_post_model_to_dto(post: Post) -> PostDTO:
    attachment = None
    logger.debug(f"post_attachment: {post.attachment}")
    if post.attachment:
        attachment = map_attachment_model_to_dto(post.attachment)
        logger.debug(f"{type(attachment)}")
    return PostDTO(
        id=post.id,
        content=post.content,
        category_id=post.category_id,
        attachment=attachment,
        user_id=post.user_id,
        status=PostStatus(post.status),
    )
