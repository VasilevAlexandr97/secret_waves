import logging

from typing import Any, ClassVar

from sqladmin import ModelView

from src.core.users.models import User

logger = logging.getLogger(__name__)

class UserView(ModelView, model=User):
    column_list: ClassVar[list[Any]] = [
        User.id,
        User.telegram_id,
        User.created_at,
    ]
