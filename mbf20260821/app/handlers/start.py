from maxapi import Router
from maxapi.types import BotStarted

from app.keyboards.general_menu import main_menu


router = Router()


@router.bot_started()
async def start_handler(event: BotStarted):

    print("BOT STARTED EVENT")

    await event.send(
        "👋 Привет!\n\n"
        "Я бот FINAM.\n"
        "Помогу получить информацию по акциям ММВБ.",
        attachments=[
            main_menu()
        ]
    )