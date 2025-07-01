from aiogram_dialog import Dialog

from src.telegram_bot.dialogs.posts.windows import (
    create_post_confirm_window,
    create_post_input_content_window,
    create_post_select_anonymity_window,
    create_post_select_category_window,
)

create_post_dialog = Dialog(
    create_post_input_content_window,
    create_post_select_category_window,
    create_post_select_anonymity_window,
    create_post_confirm_window,
)
