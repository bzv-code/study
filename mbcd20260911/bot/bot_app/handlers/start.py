"""Обработчик /start и нажатия на кнопку «Начать» — приветствие и главное меню."""
from maxapi import Router
from maxapi.filters.command import CommandStart
from maxapi.types import BotStarted, MessageCreated

from bot_app.keyboards.main_menu import main_menu_keyboard

router = Router()


@router.bot_started()
async def bot_started(event: BotStarted) -> None:
    await event.bot.send_message(
        chat_id=event.chat_id,
        text=(
            "Добро пожаловать в «Дом цветов»!\n"
            "Отправьте /start, чтобы открыть меню."
        ),
    )


@router.message_created(CommandStart())
async def cmd_start(event: MessageCreated) -> None:
    await event.message.answer(
        text="Выбирайте букет в каталоге или загляните в свои заказы.",
        attachments=[main_menu_keyboard()],
    )
