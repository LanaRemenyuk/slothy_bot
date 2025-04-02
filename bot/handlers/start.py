from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.main_menu import main_keyboard
from utils.text import start_text

router = Router()

@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        start_text,
        reply_markup=main_keyboard()
    )