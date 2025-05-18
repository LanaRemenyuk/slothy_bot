import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.support_keyboard import support_keyboard
from utils.text import support_text

router = Router()

@router.message(Command('support'))
async def cmd_support(message: Message):
    """Перенаправление в личку к админу"""
    admin_username = os.getenv('ADMIN_USERNAME')
    
    await message.answer(
        support_text,
        reply_markup=support_keyboard
    )