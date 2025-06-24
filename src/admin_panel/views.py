from typing import Any, ClassVar

from sqladmin import ModelView

from src.core.posts.models import Category, Post
from src.core.users.models import User


class UserView(ModelView, model=User):
    column_list: ClassVar[list[Any]] = [
        User.id,
        User.telegram_id,
        User.created_at,
    ]


class CategoryView(ModelView, model=Category):
    column_list: ClassVar[list[Any]] = [Category.id, Category.name]
    form_columns: ClassVar[list[Any]] = [Category.name]
    name_plural = "Categories"


class PostView(ModelView, model=Post):
    column_list: ClassVar[list[Any]] = [
        Post.id,
        Post.content,
        Post.category_id,
        Post.category,
        Post.user_id,
        Post.user,
    ]
