from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

from utils import text

def get_back_to_management_keyboard() -> InlineKeyboardMarkup:
    """Кнопка возврата в главное меню управления"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text.back_button, callback_data='back_to_main')]
        ]
    )

def get_manage_offer_by_number_keyboard() -> InlineKeyboardMarkup:
    """Главное меню управления объявлениями"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=text.remove_offer, callback_data='show_offer_numbers'),
        InlineKeyboardButton(text=text.manage_visibility, callback_data="toggle_visibility")
    )
    builder.adjust(1)
    return builder.as_markup()

def get_offer_numbers_keyboard(numbers: list[str], per_row: int = 5) -> InlineKeyboardMarkup:
    """
    Клавиатура для удаления объявлений с кнопкой возврата
    """
    builder = InlineKeyboardBuilder()

    for num in numbers:
        builder.add(InlineKeyboardButton(text=num, callback_data=f'delete_offer_{num}'))
    
    builder.adjust(per_row)
    builder.row(InlineKeyboardButton(text=text.back_button, callback_data='back_to_main'))
    
    return builder.as_markup()

def get_visibility_management_keyboard(offers_map: dict, per_row: int = 5) -> InlineKeyboardMarkup:
    """
    Клавиатура управления видимостью с кнопкой возврата
    """
    builder = InlineKeyboardBuilder()
    
    for num, offer_data in offers_map.items():
        status_icon = "🚫" if offer_data['is_hidden'] else "✅"
        builder.add(InlineKeyboardButton(
            text=f'{status_icon}{num}',
            callback_data=f'toggle_visibility_{num}'
        ))
    
    builder.adjust(per_row)
    builder.row(InlineKeyboardButton(text=text.back_button, callback_data='back_to_main'))
    
    return builder.as_markup()