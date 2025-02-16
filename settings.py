import os

from aiogram import types
from datetime import time
from dotenv import load_dotenv

load_dotenv()

START_TIME_OF_WORK, END_TIME_OF_WORK = time(9, 0), time(21, 0)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER = 871881605

DATABASE = {
    "host": os.environ.get("POSTGRES_HOST", "postgres"),
    "database": os.environ.get("POSTGRES_DATABASE", "service"),
    "password": os.environ.get("POSTGRES_PASSWORD", "password"),
    "user": os.environ.get("POSTGRES_USER", "postgres")
}

DATABASE_FOR_TESTING = {
    "host": os.environ.get("POSTGRES_HOST", "localhost"),
    "database": os.environ.get("POSTGRES_DATABASE", "service_test"),
    "password": os.environ.get("POSTGRES_PASSWORD", "password"),
    "user": os.environ.get("POSTGRES_USER", "postgres")
}

CELERY_BROKER_URL = "redis://redis:6379/0"
TIMEZONE = "Europe/Moscow"

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
