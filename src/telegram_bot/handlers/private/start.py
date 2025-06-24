from aiogram import F, Router, types
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from dishka.integrations.aiogram import FromDishka, inject

from src.core.auth.id_providers import IdProvider
from src.core.auth.models import LoginInDTO
from src.core.auth.services import AuthService
from src.core.posts.services import PostServices
from src.telegram_bot.keyboards.default import start_kb

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

    msg = (
        "Привет! 👋 Добро пожаловать в «Тайные волны» — здесь можно спокойно и анонимно выговориться, поделиться тем, что давно носишь внутри.\n\n"
        "Это пространство, где ты можешь:\n\n"
        "• 🗣️ Выплеснуть историю, эмоцию или переживание\n"
        "• 📖 Почитать, чем делятся другие — честно, тонко, по-настоящему\n"
        "• 🌊 Выбрать категорию поста для удобного поиска\n"
        "• 🔒 Выбрать, оставить ли след, чтобы потом вернуться к своим постам\n\n"
        "Добро пожаловать на борт, пусть «Тайные волны» станут твоим надёжным спутником в мире анонимных признаний! 🌙✨"
    )
    kb = start_kb()
    await message.answer(msg, reply_markup=kb)
