from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format

from src.telegram_bot.dialogs.main.getters import main_getter
from src.telegram_bot.dialogs.main.keyboards import main_kbd
from src.telegram_bot.dialogs.main.states import Main

main_window = Window(
    Format("{message_text}"),
    main_kbd,
    state=Main.MAIN,
    getter=main_getter,
)
