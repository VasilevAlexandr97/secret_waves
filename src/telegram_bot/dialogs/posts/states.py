from aiogram.fsm.state import State, StatesGroup


class CreatePost(StatesGroup):
    input_content = State()
    select_category = State()
    select_anonymity = State()
    confirm = State()
