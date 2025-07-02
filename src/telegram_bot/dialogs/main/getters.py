from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.telegram_bot.constants.messages import MessageKeys
from src.telegram_bot.services.message_service import MessageService


@inject
async def main_getter(
    dialog_manager: DialogManager,
    message_service: FromDishka[MessageService],
    **kwargs,
):
    message = message_service.get_message(
        MessageKeys.START_ACTION_PROMPT_MESSAGE,
    )
    read_stories_button_text = message_service.get_button_text(
        MessageKeys.READ_STORIES_BUTTON,
    )
    create_post_button_text = message_service.get_button_text(
        MessageKeys.CREATE_POST_BUTTON,
    )
    return {
        "message_text": message,
        "read_stories_button": {"text": read_stories_button_text},
        "create_post_button": {"text": create_post_button_text},
    }
