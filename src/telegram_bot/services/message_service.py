from typing import Any


class MessageService:
    def __init__(self, messages_config: dict[str, Any]):
        self._messages = messages_config

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
        buttons = self._messages.get("buttons", {})
        button_config = buttons.get(button_key, {})

        if not button_config or "text" not in button_config:
            raise KeyError(f"Button with key {button_key} not found")

        return button_config["text"]
