import os
import pytz

from aiogram import types
from datetime import time
from dotenv import load_dotenv

load_dotenv()

START_TIME_OF_WORK, END_TIME_OF_WORK = time(9, 0), time(21, 0)
SALON_ID = 1

DATABASE_URL = os.environ.get("DATABASE_URL")

BOT_TOKEN = os.environ.get("BOT_TOKEN")

TIMEZONE = pytz.timezone("Asia/Tomsk")

COMMANDS = [
    types.BotCommand(
        command="start",
        description="Меню"
    ),
    types.BotCommand(
        command="services",
        description="Список услуг"
    ),
    types.BotCommand(
        command="bookings",
        description="Список бронирований"
    ),
    types.BotCommand(
        command="help",
        description="Помощь"
    ),
]

