from aiogram_dialog import Dialog, LaunchMode

from src.telegram_bot.dialogs.main.windows import main_window

main_dialog = Dialog(
    main_window,
    launch_mode=LaunchMode.ROOT,
)
