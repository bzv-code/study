from maxapi import Bot

from app.config import settings


bot = Bot(
    token=settings.MAX_TOKEN
)