import asyncio
import os

import django
import aioschedule
#
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify

    await on_startup_notify(dp)
    await set_default_commands(dp)


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        'admin_panel.admin_panel.settings'
    )
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()


async def scheduler():
    print('rick')
    aioschedule.every().second.do(send_curs_push)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(60)


if __name__ == '__main__':
    setup_django()
    from aiogram import executor
    from handlers import dp
    from handlers.users.start import send_curs_push

    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())

    executor.start_polling(dp, on_startup=on_startup)
