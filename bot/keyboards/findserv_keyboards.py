from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

from utils import text

def get_tags_keyboard(popular_tags, row_width=3):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for i in range(0, len(popular_tags), row_width):
        row = [
            InlineKeyboardButton(text=tag, callback_data=f'tag_{tag}')
            for tag in popular_tags[i:i+row_width]
        ]
        keyboard.inline_keyboard.append(row)
    
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=text.add_tag, callback_data='custom_tag')
    ])
    
    return keyboard