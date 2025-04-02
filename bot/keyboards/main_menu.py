from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils import text

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text.find_service)],
            [KeyboardButton(text=text.offer_service)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )