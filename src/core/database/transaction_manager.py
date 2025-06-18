from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession


class TransactionManagerInterface(ABC):
    """Abstract interface for transaction managers."""

    @abstractmethod
    async def __aenter__(self) -> Self:
        """Enter the async context manager."""

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the async context manager, handling commit/rollback logic."""

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction."""

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction."""


class TransactionManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            print(f"Rolling back due to exception: {exc_val}")
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        try:
            await self.session.commit()
        except Exception:
            await self.rollback() # Rollback on commit error
            raise

    async def rollback(self):
        await self.session.rollback()
