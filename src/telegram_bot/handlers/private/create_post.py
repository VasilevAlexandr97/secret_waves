from logging import getLogger

from aiogram import F, Router
from dishka.integrations.aiogram import FromDishka, inject

from src.telegram_bot.constants.messages import MessageKeys
from src.telegram_bot.filters.buttons import ButtonFilter
from src.telegram_bot.services.message_service import MessageService

logger = getLogger(__name__)
create_post_router = Router()


@create_post_router.message(ButtonFilter(MessageKeys.CREATE_POST))
@inject
async def handle_create_post(message, service: FromDishka[MessageService]):
    logger.info("HELLO, create post")
