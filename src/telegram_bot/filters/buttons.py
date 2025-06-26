from aiogram.filters import BaseFilter
from dishka.integrations.aiogram import FromDishka, inject

from src.telegram_bot.services.message_service import MessageService


class ButtonFilter(BaseFilter):
    def __init__(self, button_key: str):
        self.button_key = button_key

    @inject
    async def __call__(self, message, service: FromDishka[MessageService]):
        button_key = service.get_button_key_by_text(message.text)
        return self.button_key == button_key
