import secrets

from src.core.auth.id_providers import IdProvider
from src.core.auth.models import LoginInDTO
from src.core.database.transaction_manager import TransactionManager
from src.core.users.models import UserID
from src.core.users.repositories import UserRepositoryProtocol


class AuthService:
    def __init__(
        self,
        user_repository: UserRepositoryProtocol,
        transaction_manager: TransactionManager,
    ):
        self.user_repository = user_repository
        self.transaction_manager = transaction_manager

    async def telegram_authenticate(
        self,
        id_provider: IdProvider,
        login_in_dto: LoginInDTO,
    ) -> UserID:
        user_id = await id_provider.get_current_user_id()
        if user_id is None:
            user_id = await self.user_repository.add_user(
                user_dto=LoginInDTO(
                    telegram_id=login_in_dto.telegram_id,
                ),
            )
            await self.transaction_manager.commit()
        return user_id
