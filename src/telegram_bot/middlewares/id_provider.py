from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.core.auth.id_providers import TelegramIdProvider
from src.core.users.repositories import UserRepository


class IdProviderMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        if user := data.get("event_from_user"):
            container = data["dishka_container"]
            user_repository = await container.get(UserRepository)
            id_provider = TelegramIdProvider(
                telegram_id=user.id,
                user_repository=user_repository,
            )
            data["id_provider"] = id_provider
        return await handler(event, data)
