from abc import abstractmethod
from typing import Protocol

from src.core.users.models import UserId
from src.core.users.repositories import UserRepository


class IdProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> UserId:
        ...



class TelegramIdProvider(IdProvider):
    def __init__(
        self,
        telegram_id: int,
        user_repository: UserRepository,
    ):
        self.telegram_id = telegram_id
        self.user_repository = user_repository

    async def get_current_user_id(self) -> UserId:
        user_id = await self.user_repository.get_user_id_by_telegram_id(
            telegram_id=self.telegram_id,
        )

        if not user_id:
            raise ValueError("User not found")

        return user_id
