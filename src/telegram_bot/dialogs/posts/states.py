from aiogram.fsm.state import State, StatesGroup


class CreatePost(StatesGroup):
    INPUT_CONTENT = State()
    SELECT_CATEGORY = State()
    SELECT_ANONYMITY = State()
    CONFIRM = State()


class ReadPost(StatesGroup):
    READ = State()
