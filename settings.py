import os
import pytz

from aiogram import types
from datetime import time, timezone
from dotenv import load_dotenv

load_dotenv()

START_TIME_OF_WORK, END_TIME_OF_WORK = time(9, 0), time(21, 0)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER = 871881605

DATABASE = "data/database.db"
CELERY_BROKER_URL = "redis://localhost:6379/"
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
BOT_NAME = "MasterNameBOT"
BOT_DESCRIPTION = "Помощник мастера \"...\". user-friendly interface."
BOT_SHORT_DESCRIPTION = "Помощник для записи клиентов и управлениями их бронированиями. MVP. user-friendly."
