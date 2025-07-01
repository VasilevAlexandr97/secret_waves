# secret_waves


## alembic

Применить миграции: следующие команды:

docker compose run --rm admin uv run alembic revision --autogenerate -m "add_post_attachments_and_make_content_nullable"
docker compose run --rm admin uv run alembic upgrade head