from enum import StrEnum


class MessageKeys(StrEnum):
    # DEFAULT MESSAGES
    START_MESSAGE = "start_message"
    START_ACTION_PROMPT_MESSAGE = "start_action_prompt_message"

    # DEFAULT BUTTONS
    BACK_BUTTON = "back"
    CANCEL_BUTTON = "cancel"


    MY_STATISTICS = "my_statistics"
    HELP = "help"

    ATTACHMENT_TYPE_VOICE_MESSAGE = "attachment_type_voice_message"

    # CREATE POST MESSAGES
    CREATE_POST_INPUT_CONTENT_MESSAGE = "create_post_input_content_message"
    CREATE_POST_INVALID_CONTENT_MESSAGE = "create_post_invalid_content_message"
    CREATE_POST_SELECT_CATEGORY_MESSAGE = "create_post_select_category_message"
    CREATE_POST_SELECT_ANONYMITY_MESSAGE = "create_post_select_anonymity_message"
    CREATE_POST_FULLY_ANONYMITY_MESSAGE = "create_post_fully_anonymity_message"
    CREATE_POST_LINKED_ANONYMITY_MESSAGE = "create_post_linked_anonymity_message"
    CREATE_POST_CONFIRM_MESSAGE = "create_post_confirm_message"
    CREATE_POST_SUCCESS_MESSAGE = "create_post_success_message"
    CREATE_POST_ERROR_MESSAGE = "create_post_error_message"

    # CREATE POST BUTTONS
    CREATE_POST_BUTTON = "create_post"
    FULLY_ANONYMOUS_BUTTON = "fully_anonymous"
    LINKED_ANONYMOUS_BUTTON = "linked_anonymous"
    CREATE_POST_CONFIRM_BUTTON = "create_post_confirm"


    # READ STORIES MESSAGES

    # READ STORIES BUTTONS
    READ_STORIES_BUTTON = "read_stories"