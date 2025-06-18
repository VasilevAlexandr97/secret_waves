from abc import abstractmethod
from typing import Protocol

from src.core.database.transaction_manager import TransactionManager
from src.core.users.models import UserID
from src.core.users.repositories import UserRepository


class IdProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> UserID | None:
        ...



class TelegramIdProvider(IdProvider):
    def __init__(
        self,
        telegram_id: int,
        user_repository: UserRepository,
    ):
        self.telegram_id = telegram_id
        self.user_repository = user_repository

    async def get_current_user_id(self) -> UserID | None:
        return await self.user_repository.get_user_id_by_telegram_id(
            telegram_id=self.telegram_id,
        )

