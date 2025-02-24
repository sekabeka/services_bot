import asyncio
import logging
import settings

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from core.routers.default import router
from core.bot import bot
from core.logger import InterceptHandler
from core.scheduler import scheduler
from core.database import init_database


logging.basicConfig(handlers=[InterceptHandler()], level="INFO", force=True)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def on_startup():
    await bot.set_my_commands(
        commands=settings.COMMANDS,
        scope=None
    )
    await bot.set_my_name(name=settings.BOT_NAME)
    await bot.set_my_description(description=settings.BOT_DESCRIPTION)
    await bot.set_my_short_description(short_description=settings.BOT_SHORT_DESCRIPTION)
    pass



async def main():
    await init_database()
    #await on_startup()

    dp.include_router(router)
    setup_dialogs(dp)
    scheduler.start()

    await dp.start_polling(bot)

asyncio.run(main())
