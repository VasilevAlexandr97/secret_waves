from functools import cache

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


@cache
def start_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝 Придать огласке"),
                KeyboardButton(text="📚 Читать истории"),
            ],
            [
                KeyboardButton(text="📊 Моя статистика"),
                KeyboardButton(text="❓ Помощь"),
            ],
        ],
        resize_keyboard=True,
    )
