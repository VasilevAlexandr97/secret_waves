import logging

from aiogram import types
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.core.auth.models import LoginInDTO
from src.core.auth.services import AuthService
from src.core.posts.models import (
    AttachmentDTO,
    AttachmentType,
    PostDTO,
)
from src.core.posts.services import PostService
from src.telegram_bot.constants.messages import MessageKeys
from src.telegram_bot.dialogs.main.states import Main
from src.telegram_bot.dialogs.posts.states import CreatePost
from src.telegram_bot.services.message_service import MessageService

logger = logging.getLogger(__name__)


@inject
async def create_post_input_content_handler(
    message: types.Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    message_service: FromDishka[MessageService],
):
    logger.debug(f"message: {message}")

    if message.text is not None:
        text_length = len(message.text)
        logger.debug(f"text_length: {text_length}")
        min_length = 40
        max_length = 600

        if text_length < min_length or text_length > max_length:
            message_text = message_service.get_message(
                MessageKeys.CREATE_POST_INVALID_CONTENT_MESSAGE,
            )
            await message.answer(message_text)
            dialog_manager.show_mode = ShowMode.EDIT
            return
    file_id = None
    attachment_type = None
    if message.text is None and message.voice is not None:
        file_id = message.voice.file_id
        attachment_type = AttachmentType.VOICE

    dialog_manager.dialog_data.update(
        {
            "content": message.text,
            "attachment_type": attachment_type,
            "file_id": file_id,
        },
    )
    await dialog_manager.switch_to(CreatePost.SELECT_CATEGORY)


async def create_post_select_category_handler(
    callback_query: types.CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    item_id: str,
):
    logger.debug(f"item_id: {item_id} {type(item_id)}")
    dialog_manager.dialog_data.update({"category_id": int(item_id)})
    await dialog_manager.switch_to(CreatePost.SELECT_ANONYMITY)


async def create_post_select_anonymity_handler(
    callback_query: types.CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    is_anonymous = int(widget.widget_id.split("_")[-1])
    dialog_manager.dialog_data.update({"is_anonymous": is_anonymous})
    await dialog_manager.switch_to(CreatePost.CONFIRM)


@inject
async def create_post_confirm_handler(
    callback_query: types.CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    auth_service: FromDishka[AuthService],
    post_service: FromDishka[PostService],
    message_service: FromDishka[MessageService],
):
    post_data_dict = dialog_manager.dialog_data
    id_provider = None
    if not post_data_dict["is_anonymous"]:
        id_provider = dialog_manager.middleware_data["id_provider"]
        await auth_service.telegram_authenticate(
            id_provider=id_provider,
            login_in_dto=LoginInDTO(
                telegram_id=callback_query.from_user.id,
            ),
        )

    attachment = None
    if post_data_dict.get("attachment_type") == AttachmentType.VOICE:
        attachment = AttachmentDTO(
            id=None,
            attachment_type=AttachmentType.VOICE,
            file_id=post_data_dict["file_id"],
            post_id=0,
        )

    post_data = PostDTO(
        id=None,
        content=post_data_dict["content"],
        category_id=post_data_dict["category_id"],
        attachment=attachment,
        user_id=None,
    )

    await post_service.create_post(
        post_data=post_data,
        id_provider=id_provider,
    )
    success_message = message_service.get_message(
        MessageKeys.CREATE_POST_SUCCESS_MESSAGE,
    )
    await callback_query.message.answer(text=success_message)
    await dialog_manager.start(
        Main.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
