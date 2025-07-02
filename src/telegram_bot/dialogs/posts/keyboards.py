import operator

from aiogram_dialog import ShowMode, StartMode
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    Select,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Format

from src.telegram_bot.constants.messages import MessageKeys
from src.telegram_bot.dialogs.main.states import Main
from src.telegram_bot.dialogs.posts.handlers import (
    create_post_confirm_handler,
    create_post_select_anonymity_handler,
    create_post_select_category_handler,
)
from src.telegram_bot.dialogs.posts.states import CreatePost

create_post_input_content_kbd = Group(
    Start(
        Format("{cancel_button[text]}"),
        id="create_post_cancel_button",
        state=Main.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    ),
)

create_post_categories_kbd = Group(
    Group(
        Select(
            Format("{item.name}"),
            id="create_post_select_category",
            item_id_getter=operator.attrgetter("id"),
            items="categories",
            on_click=create_post_select_category_handler,
        ),
        width=2,
    ),
    SwitchTo(
        text=Format("{back_button[text]}"),
        id="create_post_back_button",
        state=CreatePost.INPUT_CONTENT,
    ),
    Start(
        Format("{cancel_button[text]}"),
        id="create_post_cancel_button",
        state=Main.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    ),
)


create_post_anonymity_types_kbd = Group(
    Group(
        Button(
            Format("{fully_anonymous_button[text]}"),
            id="create_post_is_anonymous_1",
            on_click=create_post_select_anonymity_handler,
        ),
        Button(
            Format("{linked_anonymous_button[text]}"),
            id="create_post_is_anonymous_0",
            on_click=create_post_select_anonymity_handler,
        ),
        width=2,
    ),
    SwitchTo(
        text=Format("{back_button[text]}"),
        id="create_post_back_button",
        state=CreatePost.SELECT_CATEGORY,
    ),
    Start(
        Format("{cancel_button[text]}"),
        id="create_post_cancel_button",
        state=Main.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    ),
)


create_post_confirm_kbd = Group(
    Button(
        Format("{confirm_button[text]}"),
        id=MessageKeys.CREATE_POST_CONFIRM_BUTTON,
        on_click=create_post_confirm_handler,
    ),
    SwitchTo(
        text=Format("{back_button[text]}"),
        id="create_post_back_button",
        state=CreatePost.SELECT_ANONYMITY,
    ),
    Start(
        Format("{cancel_button[text]}"),
        id="create_post_cancel_button",
        state=Main.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    ),
)
