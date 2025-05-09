from aiogram import F, Router
from aiogram.types import Message

from utils import text
from keyboards.findserv_keyboards import get_tags_keyboard
from services.postgres import get_popular_tags

router = Router()

@router.message(F.text == text.find_service)
async def start_service_search(message: Message):
    """В начале поиска услуги показываем популярные теги: можно выбрать
    из существующих либо ввести свой"""
    popular_tags = await get_popular_tags()
    await message.answer(
        text.choose_tag,
        reply_markup=get_tags_keyboard(popular_tags)
    )
