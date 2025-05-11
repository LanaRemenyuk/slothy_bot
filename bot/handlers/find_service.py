import logging
import os

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv
from redis.asyncio import Redis

from utils import text
from keyboards.findserv_keyboards import get_tags_keyboard, create_navigation_buttons
from services.postgres import get_popular_tags, get_offers_by_tag
from services.redis import RedisSessionManager
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
load_dotenv()

router = Router()


logger = logging.getLogger(__name__)

# Инициализация Redis клиента
redis_client = Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    db=os.getenv('REDIS_DB'),
    decode_responses=False
)
# Создание менеджера сессий Redis
session_manager = RedisSessionManager(redis_client)

@router.message(F.text == text.find_service)
async def start_service_search(message: Message):
    """В начале поиска услуги показываем популярные теги: можно выбрать
    из существующих либо ввести свой"""
    popular_tags = await get_popular_tags()
    await message.answer(
        text.choose_tag,
        reply_markup=get_tags_keyboard(popular_tags)
    )

@router.callback_query(F.data.startswith('tag_'))
async def process_tag_selection(query: CallbackQuery):
    try:
        user_id = query.from_user.id
        tag = query.data.replace('tag_', '')

        if not await session_manager.session_exists(user_id, tag):
            offers = await get_offers_by_tag(tag)
            if not offers:
                await query.message.answer(text.no_offers)
                await query.answer()
                return
      
            await session_manager.init_session(user_id, tag, offers)

        await _display_current_offer(query, user_id, tag)
        
    except Exception as e:
        logger.error(f'Tag selection error: {e}', exc_info=True)
        await query.message.answer(text.tag_error)
        await query.answer()

async def _display_current_offer(query: CallbackQuery, user_id: int, tag: str):
    current_offer = await session_manager.get_current_offer(user_id, tag)
    if not current_offer:
        await query.message.answer(text.offer_upload_failed)
        await query.answer()
        return

    current_index = await session_manager.get_current_index(user_id, tag)
    total_offers = await session_manager.get_total_offers(user_id, tag)
    keyboard = create_navigation_buttons(current_index, total_offers)
    offer_text = text.format_offer(tag, current_offer)

    if query.message.text:
        await query.message.edit_text(offer_text, reply_markup=keyboard)
    else:
        await query.message.answer(offer_text, reply_markup=keyboard)
    
    await query.answer()

@router.callback_query(F.data.in_(['prev_offer', 'next_offer']))
async def handle_offer_navigation(query: CallbackQuery):
    try:
        user_id = query.from_user.id
        tag = await session_manager.get_active_tag(user_id)
        if not tag:
            await query.answer(text.session_expired, show_alert=True)
            return
        
        if query.data == 'prev_offer':
            await session_manager.decrement_index(user_id, tag)
        else:
            await session_manager.increment_index(user_id, tag)
        
        await _display_current_offer(query, user_id, tag)
    
    except Exception as e:
        logger.error(f'Ошибка при поиске объявления: {e}', exc_info=True)
        await query.answer(text.nav_error, show_alert=True)


@router.callback_query(F.data == 'custom_tag')
async def handle_custom_tag(query: CallbackQuery):
    await query.message.answer(text.enter_custom_tag)
    await query.answer()

@router.message(F.text & ~F.text.startswith('/'))
async def process_custom_tag(message: Message):
    try:
        user_id = message.from_user.id
        tag = message.text.strip()
        
        if not tag:
            await message.answer(text.empty_tag)
            return
            
        if not await session_manager.session_exists(user_id, tag):
            offers = await get_offers_by_tag(tag)
            if not offers:
                await message.answer(text.no_offers_for_custom_tag.format(tag))
                return
                
            await session_manager.init_session(user_id, tag, offers)
        
        current_offer = await session_manager.get_current_offer(user_id, tag)
        if not current_offer:
            await message.answer(text.offer_upload_failed)
            return

        current_index = await session_manager.get_current_index(user_id, tag)
        total_offers = await session_manager.get_total_offers(user_id, tag)
        keyboard = create_navigation_buttons(current_index, total_offers)
        
        offer_text = text.format_offer(tag, current_offer)
        
        await message.answer(offer_text, reply_markup=keyboard)
        
    except Exception as e:
        logger.error(f'Ошибка при обработке пользовательского тега: {e}', exc_info=True)
        await message.answer(text.tag_error)