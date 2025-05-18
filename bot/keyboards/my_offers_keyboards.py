from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

def get_offers_keyboard(offers: list[dict]) -> InlineKeyboardMarkup:
    """Клавиатура для списка объявлений"""
    builder = InlineKeyboardBuilder()
    
    for offer in offers:
        builder.button(
            text=offer.get('service_type', ['Без тега'])[0],
            callback_data=f"show_offer_{offer['id']}"
        )
    
    builder.adjust(2)
    return builder.as_markup()


def get_pagination_keyboard(page: int, total_pages: int) -> InlineKeyboardMarkup:
    """Клавиатура пагинации"""
    builder = InlineKeyboardBuilder()
    
    if page > 0:
        builder.button(text="⬅️ Назад", callback_data=f"prev_page_{page}")
    
    builder.button(text=f"{page+1}/{total_pages}", callback_data="current_page")
    
    if page < total_pages - 1:
        builder.button(text="Вперед ➡️", callback_data=f"next_page_{page}")
    
    return builder.as_markup()