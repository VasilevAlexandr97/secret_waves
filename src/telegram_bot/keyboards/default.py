from functools import cache

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.telegram_bot.constants.messages import MessageKeys
from src.telegram_bot.services.message_service import MessageService


@cache
def create_main_menu_keyboard(
    message_service: MessageService,
) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=message_service.get_button_text(MessageKeys.CREATE_POST)),
                KeyboardButton(text=message_service.get_button_text(MessageKeys.READ_STORIES)),
            ],
            [
                KeyboardButton(text=message_service.get_button_text(MessageKeys.MY_STATISTICS)),
                KeyboardButton(text=message_service.get_button_text(MessageKeys.HELP)),
            ],
        ],
        resize_keyboard=True,
    )
