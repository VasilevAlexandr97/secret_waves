from aiogram import F, Router, types
from aiogram.enums import ChatType
from aiogram_dialog import DialogManager, StartMode, ShowMode

from src.telegram_bot.constants.messages import MessageKeys
from src.telegram_bot.dialogs.posts.states import CreatePost
from src.telegram_bot.filters.buttons import ButtonFilter

posts_router = Router()
posts_router.message.filter(F.chat.type == ChatType.PRIVATE)


@posts_router.callback_query(F.data == MessageKeys.CREATE_POST_BUTTON)
@posts_router.message(ButtonFilter(MessageKeys.CREATE_POST_BUTTON))
async def create_post_handler(
    message: types.Message | types.CallbackQuery,
    dialog_manager: DialogManager,
):
    await dialog_manager.start(
        CreatePost.input_content,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
