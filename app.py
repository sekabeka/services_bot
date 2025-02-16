import asyncio
import logging
import settings

from aiogram import Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from core.routers.default import router
from core.bot import bot
from core.logger import InterceptHandler


logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def on_startup():
    # await bot.set_my_commands(
    #     commands=settings.COMMANDS,
    #     scope=None
    # )
    # await bot.set_my_name(name=settings.BOT_NAME)
    # await bot.set_my_description(description=settings.BOT_DESCRIPTION)
    # await bot.set_my_short_description(short_description=settings.BOT_SHORT_DESCRIPTION)
    pass


async def main():
    dp.include_router(router)
    setup_dialogs(dp)
    await on_startup()
    await dp.start_polling(bot)

asyncio.run(main())