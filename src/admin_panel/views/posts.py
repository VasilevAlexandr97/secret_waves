import logging

from typing import Any, ClassVar

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from markupsafe import Markup
from sqladmin import BaseView, ModelView, expose
from starlette.requests import Request
from wtforms import SelectField

from src.admin_panel.filters import PostStatusFilter
from src.core.posts.models import (
    Attachment,
    Category,
    Post,
    PostId,
    PostStatus,
)
from src.core.posts.services import PostService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin/posts", tags=["Posts"])


class CategoryView(ModelView, model=Category):
    column_list: ClassVar[list[Any]] = [Category.id, Category.name]
    form_columns: ClassVar[list[Any]] = [Category.name]
    name_plural = "Categories"


class PostView(ModelView, model=Post):
    column_list: ClassVar[list[Any]] = [
        Post.id,
        Post.content,
        Post.category_id,
        Post.status,
        Post.category,
        Post.attachment,
        Post.user_id,
        Post.user,
    ]
    column_formatters: ClassVar[dict[Any, Any]] = {
        Post.content: lambda m, _: m.content[:20] if m.content else "",
        Post.category: lambda m, _: m.category.name,
        Post.status: lambda m, _: {
            PostStatus.APPROVED: "Одобрен",
            PostStatus.REJECTED: "Отклонен",
            PostStatus.PENDING: "Ожидает",
        }.get(m.status, m.status),
    }
    column_formatters_detail: ClassVar[dict[Any, Any]] = {
        Post.content: lambda m, _: Markup(
            (
                "<div style='white-space: pre-wrap; font-family: inherit;'>"
                "{}"
                "</div>"
            ),
        ).format(m.content) if m.content else "",
    }

    column_filters: ClassVar[list[Any]] = [PostStatusFilter()]

    form_overrides: ClassVar[dict[Any, Any]] = {
        "status": SelectField,
    }
    form_args: ClassVar[dict[Any, Any]] = {
        "status": {
            "choices": [
                (PostStatus.APPROVED, "Одобрен"),
                (PostStatus.REJECTED, "Отклонен"),
                (PostStatus.PENDING, "Ожидает"),
            ],
            "coerce": str,
        },
    }


class AttachmentView(ModelView, model=Attachment):
    column_list: ClassVar[list[Any]] = [
        Attachment.id,
        Attachment.attachment_type,
        Attachment.file_id,
        Attachment.post_id,
        Attachment.post,
    ]

class ModerationPostView(BaseView):
    name = "Moderation Posts"

    @expose("/moderation_posts/", methods=["GET"])
    async def moderation_posts_page(self, request: Request):
        container = request.scope["state"]["dishka_container"]
        async with container() as r_c:
            post_service: PostService = await r_c.get(PostService)
            result = await post_service.get_pending_posts(limit=50, offset=0)
            return await self.templates.TemplateResponse(
                request,
                "moderation_posts.html",
                context={
                    "posts": result.items,
                    "count_posts": result.count,
                },
            )


@router.get("/approve/{post_id}")
@inject
async def approve_post(post_id: PostId, post_service: FromDishka[PostService]):
    await post_service.approve_post(post_id)
    return RedirectResponse(url="/admin/moderation_posts/")


@router.get("/reject/{post_id}")
@inject
async def reject_post(post_id: PostId, post_service: FromDishka[PostService]):
    await post_service.reject_post(post_id)
    return RedirectResponse(url="/admin/moderation_posts/")
