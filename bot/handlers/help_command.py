from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils import help_text

router = Router()

@router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer(
        help_text.help_text,
    )