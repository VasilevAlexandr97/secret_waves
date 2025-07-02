from aiogram.types import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Format

from src.telegram_bot.dialogs.posts.getters import (
    create_post_confirm_getter,
    create_post_input_content_getter,
    create_post_select_anonymity_getter,
    create_post_select_category_getter,
)
from src.telegram_bot.dialogs.posts.handlers import (
    create_post_input_content_handler,
)
from src.telegram_bot.dialogs.posts.keyboards import (
    create_post_anonymity_types_kbd,
    create_post_categories_kbd,
    create_post_confirm_kbd,
    create_post_input_content_kbd,
)
from src.telegram_bot.dialogs.posts.states import CreatePost

create_post_input_content_window = Window(
    Format("{message_text}"),
    MessageInput(
        create_post_input_content_handler,
        content_types=[ContentType.TEXT, ContentType.VOICE],
    ),
    create_post_input_content_kbd,
    getter=create_post_input_content_getter,
    state=CreatePost.INPUT_CONTENT,
)


create_post_select_category_window = Window(
    Format("{message_text}"),
    create_post_categories_kbd,
    getter=create_post_select_category_getter,
    state=CreatePost.SELECT_CATEGORY,
)


create_post_select_anonymity_window = Window(
    Format("{message_text}"),
    create_post_anonymity_types_kbd,
    getter=create_post_select_anonymity_getter,
    state=CreatePost.SELECT_ANONYMITY,
)


create_post_confirm_window = Window(
    Format("{message_text}"),
    create_post_confirm_kbd,
    getter=create_post_confirm_getter,
    state=CreatePost.CONFIRM,
)

