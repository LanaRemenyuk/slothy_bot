from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from utils import text

def get_delete_offer_by_number_keyboard() -> InlineKeyboardMarkup:
    """Кнопка перехода к удалению объявлений"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text.remove_offer, callback_data='show_offer_numbers')]
        ]
    )


def get_offer_numbers_keyboard(numbers: list[str], per_row: int = 5) -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру с номерами объявлений для удаления.

    :param numbers: список номеров как строки, например ['1', '2', '3']
    :param per_row: количество кнопок в одной строке
    :return: InlineKeyboardMarkup
    """
    buttons = [
        InlineKeyboardButton(text=num, callback_data=f'delete_offer_{num}')
        for num in numbers
    ]
    rows = [buttons[i:i + per_row] for i in range(0, len(buttons), per_row)]
    return InlineKeyboardMarkup(inline_keyboard=rows)