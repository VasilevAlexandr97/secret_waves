from typing import Protocol

from src.core.users.models import User, UserDTO


class UserMapperProtocol(Protocol):
    def to_dto(
        self,
        model: User,
    ) -> UserDTO:
        pass

    def to_model(
        self,
        dto: UserDTO,
    ) -> User:
        pass


class UserMapper:
    def to_dto(
        self,
        model: User,
    ) -> UserDTO:
        return UserDTO(
            id=model.id,
            telegram_id=model.telegram_id,
            username=model.username,
        )

    def to_model(
        self,
        dto: UserDTO,
    ) -> User:
        return User(
            id=dto.id,
            telegram_id=dto.telegram_id,
            username=dto.username,
        )
