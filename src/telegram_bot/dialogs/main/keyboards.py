from aiogram_dialog import StartMode
from aiogram_dialog.widgets.kbd import Group, Start
from aiogram_dialog.widgets.text import Format

from src.telegram_bot.dialogs.posts.states import CreatePost

main_kbd = Group(
    Start(
        Format("{read_stories_button[text]}"),
        id="read_stories_button",
        state=CreatePost,
    ),
    Start(
        Format("{create_post_button[text]}"),
        id="create_post_button",
        state=CreatePost.INPUT_CONTENT,
        # mode=StartMode.RESET_STACK,
    ),
)
