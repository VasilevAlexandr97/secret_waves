from src.core.posts.models import Post, PostStatus


class PostStatusFilter:
    title: str = "POST STATUS"
    parameter_name: str = "status"

    async def lookups(self, request, model, run_query) -> list[tuple[str, str]]:
        return (
            ("all", "Все"),
            (PostStatus.APPROVED, "Одобрен"),
            (PostStatus.REJECTED, "Отклонен"),
            (PostStatus.PENDING, "Ожидает"),
        )

    async def get_filtered_query(self, query, value, model):
        if value in PostStatus:
            return query.filter(model.status == value)
        return query
