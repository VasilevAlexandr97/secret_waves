import logging

from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Button:
    text: str

class MessageService:
    def __init__(self, messages_config: dict[str, Any]):
        self._messages = messages_config
        self._buttons_cache: dict[str, Button] = {}
        self._button_text_to_key_cache: dict[str, str] = {}
        self._build_buttons_cache()
        self._build_button_text_to_key_cache()
        logger.info("MessageService initialized")
        logger.info(f"Messages: {self._messages}")
        logger.info(f"Buttons cache: {self._buttons_cache}")
        logger.info(
            f"Button text to key cache: {self._button_text_to_key_cache}"
        )

    def get_message(self, key: str) -> str:
        """
        Получает сообщение по ключу
        """
        if key not in self._messages:
            raise KeyError(f"Message with key {key} not found")
        return self._messages[key]

    def get_button_text(self, button_key: str) -> str:
        """
        Получает текст кнопки по ключу
        """
        return self._buttons_cache[button_key].text

    def get_button_key_by_text(self, button_text: str) -> str | None:
        """
        Получает ключ кнопки по тексту
        """
        return self._button_text_to_key_cache.get(button_text)

    def _build_buttons_cache(self) -> None:
        self._buttons_cache.clear()

        buttons: dict[str, dict] = self._messages.get("buttons", {})
        for button_key, button_config in buttons.items():
            if isinstance(button_config, dict) and "text" in button_config:
                button = Button(
                    text=button_config["text"],
                )
                self._buttons_cache[button_key] = button

    def _build_button_text_to_key_cache(self) -> None:
        """
        Строит кэш для быстрого получения ключа кнопки по тексту
        """
        self._button_text_to_key_cache.clear()

        buttons = self._messages.get("buttons", {})
        for button_key, button_config in buttons.items():
            if isinstance(button_config, dict) and "text" in button_config:
                button_text = button_config["text"]
                self._button_text_to_key_cache[button_text] = button_key
