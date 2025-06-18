from aiogram import F, Router, types
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from dishka.integrations.aiogram import FromDishka, inject

from src.core.auth.id_providers import IdProvider
from src.core.auth.models import LoginInDTO
from src.core.auth.services import AuthService

start_router = Router()
start_router.message.filter(F.chat.type == ChatType.PRIVATE)

@start_router.message(CommandStart())
@inject
async def command_start_handler(
    message: types.Message,
    auth_service: FromDishka[AuthService],
    id_provider: IdProvider,
):
    await auth_service.telegram_authenticate(
        id_provider=id_provider,
        login_in_dto=LoginInDTO(
            telegram_id=message.from_user.id,
        ),
    )
    # await auth_service.get_or_create_user_by_telegram(
    #     telegram_id=message.from_user.id,
    # )
    await message.answer(
        "Hello! I'm a bot. To get started, please use the /start command."
    )

