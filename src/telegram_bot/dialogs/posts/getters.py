import logging

from aiogram_dialog import DialogManager
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.core.posts.models import AttachmentType
from src.core.posts.services import PostService
from src.telegram_bot.constants.messages import MessageKeys
from src.telegram_bot.services.message_service import MessageService

logger = logging.getLogger(__name__)


@inject
async def create_post_input_content_getter(
    dialog_manager: DialogManager,
    message_service: FromDishka[MessageService],
    **kwargs,
):
    message = message_service.get_message(
        MessageKeys.CREATE_POST_INPUT_CONTENT_MESSAGE,
    )
    cancel_button_text = message_service.get_button_text(
        MessageKeys.CANCEL_BUTTON,
    )
    return {
        "message_text": message,
        "cancel_button": {"text":cancel_button_text},
    }


@inject
async def create_post_select_category_getter(
    dialog_manager: DialogManager,
    posts_service: FromDishka[PostService],
    message_service: FromDishka[MessageService],
    **kwargs,
):
    message = message_service.get_message(
        MessageKeys.CREATE_POST_SELECT_CATEGORY_MESSAGE,
    )
    back_button_text = message_service.get_button_text(
        MessageKeys.BACK_BUTTON,
    )
    cancel_button_text = message_service.get_button_text(
        MessageKeys.CANCEL_BUTTON,
    )
    categories = await posts_service.get_categories()
    return {
        "message_text": message,
        "categories": categories,
        "back_button": {"text": back_button_text},
        "cancel_button": {"text": cancel_button_text},
    }


@inject
async def create_post_select_anonymity_getter(
    dialog_manager: DialogManager,
    message_service: FromDishka[MessageService],
    **kwargs,
):
    message = message_service.get_message(
        MessageKeys.CREATE_POST_SELECT_ANONYMITY_MESSAGE,
    )
    fully_anonymous = message_service.get_button_text(
        MessageKeys.FULLY_ANONYMOUS_BUTTON,
    )
    linked_anonymous = message_service.get_button_text(
        MessageKeys.LINKED_ANONYMOUS_BUTTON,
    )
    back_button_text = message_service.get_button_text(
        MessageKeys.BACK_BUTTON,
    )
    cancel_button_text = message_service.get_button_text(
        MessageKeys.CANCEL_BUTTON,
    )
    return {
        "message_text": message,
        "fully_anonymous_button": {
            "is_anonymous": 1,
            "text": fully_anonymous,
        },
        "linked_anonymous_button": {
            "is_anonymous": 0,
            "text": linked_anonymous,
        },
        "back_button": {"text": back_button_text},
        "cancel_button": {"text": cancel_button_text},
    }


@inject
async def create_post_confirm_getter(
    dialog_manager: DialogManager,
    message_service: FromDishka[MessageService],
    post_service: FromDishka[PostService],
    **kwargs,
):
    post_data = dialog_manager.dialog_data
    logger.debug(f"post_data: {post_data}")
    category = await post_service.get_category_by_id(post_data["category_id"])

    is_anonymous = post_data["is_anonymous"]
    if is_anonymous:
        is_anonymous_text = message_service.get_message(
            MessageKeys.CREATE_POST_FULLY_ANONYMITY_MESSAGE,
        )
    else:
        is_anonymous_text = message_service.get_message(
            MessageKeys.CREATE_POST_LINKED_ANONYMITY_MESSAGE,
        )

    if post_data.get("attachment_type") == AttachmentType.VOICE:
        content = message_service.get_message(
            MessageKeys.ATTACHMENT_TYPE_VOICE_MESSAGE,
        )
    else:
        content = post_data["content"]

    message = message_service.get_message(
        MessageKeys.CREATE_POST_CONFIRM_MESSAGE,
    ).format(
        category=category.name,
        is_anonymous=is_anonymous_text,
        content=content,
    )
    confirm_button_text = message_service.get_button_text(
        MessageKeys.CREATE_POST_CONFIRM_BUTTON,
    )
    back_button_text = message_service.get_button_text(
        MessageKeys.BACK_BUTTON,
    )
    cancel_button_text = message_service.get_button_text(
        MessageKeys.CANCEL_BUTTON,
    )
    return {
        "message_text": message,
        "confirm_button": {
            "text": confirm_button_text,
        },
        "back_button": {"text": back_button_text},
        "cancel_button": {"text": cancel_button_text},
    }