import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.postgres import get_user_offers
from utils.text import no_active_offers, format_own_offer, offers_error

router = Router()

logger = logging.getLogger(__name__)

@router.message(Command('myoffers'))
async def cmd_myoffers(message: Message):
    """Вывод всех объявлений пользователя"""
    try:
        user_id = message.from_user.id
        offers = await get_user_offers(user_id)

        if not offers:
            await message.answer(no_active_offers)
            return
        
        all_offers_text = ""
        for offer in offers:
            all_offers_text += format_own_offer(offer) + "\n\n"

        await message.answer(all_offers_text)

    except Exception as e:
        logger.error(f'Error in myoffers: {e}')
        await message.answer(offers_error)