from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.telegram_bot.constants.messages import MessageKeys
from src.telegram_bot.services.message_service import MessageService


def create_start_action_inline_kbd(
    message_service: MessageService,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=message_service.get_button_text(MessageKeys.READ_STORIES_BUTTON),
        callback_data=MessageKeys.READ_STORIES_BUTTON,
    )
    keyboard.button(
        text=message_service.get_button_text(MessageKeys.CREATE_POST_BUTTON),
        callback_data=MessageKeys.CREATE_POST_BUTTON,
    )
    keyboard.adjust(1, 1)
    return keyboard.as_markup()
