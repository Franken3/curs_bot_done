from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("curs", "Рандомно генерирует курс для валют в пределах +- 5 рублей от настоящего"),
    ])
