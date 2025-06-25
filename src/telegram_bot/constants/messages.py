from enum import StrEnum


class MessageKeys(StrEnum):
    START_MESSAGE = "start_message"
    BUTTONS = "buttons"

    # Кнопки
    CREATE_POST = "create_post"
    READ_STORIES = "read_stories"
    MY_STATISTICS = "my_statistics"
    HELP = "help"
