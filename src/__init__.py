from src.main.admin import create_admin_app
from src.main.tg_bot import create_tgbot_app

admin_app = create_admin_app()
bot, dp = create_tgbot_app()
