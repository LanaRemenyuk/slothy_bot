import os

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from dotenv import load_dotenv

from utils import text

load_dotenv()

support_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text.contact_admin,
                    url=f'tg://resolve?domain={os.getenv("ADMIN_USERNAME")}'
                )
            ]
        ]
    )