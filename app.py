import asyncio
import logging

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

async def main():
    await init_database()

    dp.include_router(router)
    setup_dialogs(dp)
    scheduler.start()

    await dp.start_polling(bot)

asyncio.run(main())
