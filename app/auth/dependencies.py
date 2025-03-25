from easy_async_tg_notify import Notifier

from app.config import settings


async def get_notifier():
    async with Notifier(settings.BOT_TOKEN) as notifier:
        yield notifier


def get_current_admin_user():
    return None