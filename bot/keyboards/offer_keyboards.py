from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from utils import text


def get_confirmation_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text.yes)],
            [KeyboardButton(text=text.no)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text.send_phone, request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def get_existing_tags():
    return text.base_tags

def get_tags_keyboard(existing_tags: list[str], selected_tags: list[str] = None, show_done_button: bool = False) -> InlineKeyboardMarkup:
    if selected_tags is None:
        selected_tags = []
    
    buttons = []
    for tag in existing_tags:
        prefix = "✅ " if tag in selected_tags else ""
        buttons.append(
            InlineKeyboardButton(text=f"{prefix}{tag}", callback_data=f"tag_{tag}")
        )
    
    keyboard = [buttons[i:i+3] for i in range(0, len(buttons), 3)]
    
    if show_done_button:
        row = []
        if selected_tags:
            row.append(InlineKeyboardButton(text="🚀 Готово", callback_data="done_tags"))
        row.append(InlineKeyboardButton(text="✏️ Ввести свой", callback_data="add_custom_tag"))
        keyboard.append(row)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_to_tags_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_tags")]
    ])