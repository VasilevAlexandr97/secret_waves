from aiogram import F, Router, types
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode
from dishka.integrations.aiogram import FromDishka, inject

from src.core.auth.id_providers import IdProvider
from src.core.auth.models import LoginInDTO
from src.core.auth.services import AuthService
from src.telegram_bot.constants.messages import MessageKeys
from src.telegram_bot.dialogs.main.states import Main
from src.telegram_bot.keyboards.default import create_main_menu_reply_kbd
from src.telegram_bot.services.message_service import MessageService

start_router = Router()
start_router.message.filter(F.chat.type == ChatType.PRIVATE)

@start_router.message(CommandStart())
@inject
async def start_command_handler(
    message: types.Message,
    auth_service: FromDishka[AuthService],
    message_service: FromDishka[MessageService],
    id_provider: IdProvider,
    dialog_manager: DialogManager,
):
    await auth_service.telegram_authenticate(
        id_provider=id_provider,
        login_in_dto=LoginInDTO(
            telegram_id=message.from_user.id,
        ),
    )
    strt_message_text = message_service.get_message(MessageKeys.START_MESSAGE)
    start_keyboard = create_main_menu_reply_kbd(message_service)
    await message.answer(strt_message_text, reply_markup=start_keyboard)
    await dialog_manager.start(Main.MAIN, mode=StartMode.RESET_STACK)
