import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from services.postgres import get_user_offers, delete_offer_by_id
from keyboards.my_offers_keyboards import get_delete_offer_by_number_keyboard, get_offer_numbers_keyboard
from utils import text as texts

from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

router = Router()

logger = logging.getLogger(__name__)


user_offer_map = {}

@router.message(Command('myoffers'))
async def cmd_myoffers(message: Message):
    """Вывод всех объявлений пользователя"""
    try:
        user_id = message.from_user.id
        offers = await get_user_offers(user_id)

        if not offers:
            await message.answer(texts.no_active_offers)
            return

        user_offer_map[user_id] = {}  # Сохраняем соответствие номер → offer_id
        text = "Ваши объявления:\n\n"
        for idx, offer in enumerate(offers, start=1):
            user_offer_map[user_id][str(idx)] = offer['id']
            text += f"{idx}. {texts.format_own_offer(offer)}\n\n"

        del_keyboard = get_delete_offer_by_number_keyboard()

        await message.answer(text.strip(), reply_markup=del_keyboard)

    except Exception as e:
        await message.answer(texts.offers_error)

# Показываем кнопки с номерами
@router.callback_query(F.data == 'show_offer_numbers')
async def show_offer_number_buttons(callback: CallbackQuery):
    user_id = callback.from_user.id
    offers_map = user_offer_map.get(user_id)

    if not offers_map:
        await callback.answer(texts.no_active_offers)
        return

    nums_keyboard = get_offer_numbers_keyboard(list(offers_map.keys()))

    await callback.message.edit_reply_markup(reply_markup=nums_keyboard)

# Обработка удаления по номеру
@router.callback_query(F.data.startswith("delete_offer_"))
async def delete_selected_offer(callback: CallbackQuery):
    user_id = callback.from_user.id
    selected_num = callback.data.split("_")[-1]
    offer_id = user_offer_map.get(user_id, {}).get(selected_num)

    if not offer_id:
        await callback.answer(texts.offer_not_found)
        return

    try:
        await delete_offer_by_id(offer_id)
        await callback.message.edit_text(texts.offer_deleted_message(selected_num))
    except Exception as e:
        await callback.message.edit_text(texts.deletion_error)