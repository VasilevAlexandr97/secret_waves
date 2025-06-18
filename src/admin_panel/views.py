from sqladmin import ModelView

from src.core.posts.models import Category, Post
from src.core.users.models import User


class UserView(ModelView, model=User):
    column_list = [User.id, User.telegram_id, User.created_at]


class CategoryView(ModelView, model=Category):
    column_list = [Category.id, Category.name, Category.posts]

class PostView(ModelView, model=Post):
    column_list = [Post.id, Post.content, Post.category_id, Post.category, Post.user_id, Post.user]
    