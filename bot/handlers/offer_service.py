from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from keyboards import offer_keyboards
from services.postgres import save_to_db
from states.offer_state import OfferService
from utils import text

router = Router()

@router.message(F.text == text.offer_service)
async def offer_service_start(message: Message, state: FSMContext):
    await state.update_data(selected_tags=[])
    await message.answer(
        text.personal_data,
        reply_markup=offer_keyboards.get_confirmation_keyboard()
    )
    await state.set_state(OfferService.confirm_data)

@router.message(OfferService.confirm_data, F.text == text.yes)
async def process_confirm_yes(message: Message, state: FSMContext):
    await message.answer(
        text.tg_nick,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OfferService.telegram_nick)

@router.message(OfferService.confirm_data, F.text == text.no)
async def process_confirm_no(message: Message, state: FSMContext):
    await message.answer(
        text.data_needed,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()

@router.message(OfferService.telegram_nick)
async def process_nick(message: Message, state: FSMContext):
    await state.update_data(telegram_nick=message.text)
    await message.answer(
        text.share_phone,
        reply_markup=offer_keyboards.get_phone_keyboard()
    )
    await state.set_state(OfferService.phone)

@router.message(OfferService.phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(
        text.full_name,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OfferService.full_name)

@router.message(OfferService.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    existing_tags = await offer_keyboards.get_existing_tags()
    keyboard = offer_keyboards.get_tags_keyboard(existing_tags, [], True)
    await message.answer(
        "Выберите до 3 тегов или введите свои:",
        reply_markup=keyboard
    )
    await state.set_state(OfferService.service_type)

@router.callback_query(F.data.startswith('tag_'), OfferService.service_type)
async def process_tag_selection(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    selected_tags = user_data.get('selected_tags', [])
    custom_tags = user_data.get('custom_tags', [])
    total_tags = len(selected_tags) + len(custom_tags)
    selected_tag = callback.data.replace('tag_', '')

    if selected_tag in selected_tags:
        selected_tags.remove(selected_tag)
    elif total_tags < 3:
        selected_tags.append(selected_tag)
    else:
        await callback.answer("Можно выбрать не более 3 тегов", show_alert=True)
        return

    await state.update_data(selected_tags=selected_tags)
    await update_tags_message(callback, state)
    await callback.answer()

@router.callback_query(F.data == "add_custom_tag", OfferService.service_type)
async def process_add_custom_tag(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    total_tags = len(user_data.get('selected_tags', [])) + len(user_data.get('custom_tags', []))
    
    if total_tags >= 3:
        await callback.answer("Уже выбрано максимальное количество тегов", show_alert=True)
        return

    await callback.message.edit_text(
        "Введите свой тег (или несколько через запятую):",
        reply_markup=offer_keyboards.get_back_to_tags_keyboard()
    )
    await state.set_state(OfferService.custom_tag_input)

@router.callback_query(F.data == "back_to_tags", OfferService.custom_tag_input)
async def process_back_to_tags(callback: CallbackQuery, state: FSMContext):
    await update_tags_message(callback, state)
    await state.set_state(OfferService.service_type)

@router.message(OfferService.custom_tag_input)
async def process_custom_tag_input(message: Message, state: FSMContext):
    user_data = await state.get_data()
    selected_tags = user_data.get('selected_tags', [])
    custom_tags = user_data.get('custom_tags', [])
    total_tags = len(selected_tags) + len(custom_tags)
    input_tags = [tag.strip() for tag in message.text.split(',') if tag.strip()]
    available_slots = 3 - total_tags

    if len(input_tags) > available_slots:
        await message.answer(f"Можно добавить только {available_slots} тега(ов)")
        return

    new_custom_tags = custom_tags + input_tags[:available_slots]
    await state.update_data(custom_tags=new_custom_tags)
    await update_tags_message(message, state)
    await state.set_state(OfferService.service_type)

@router.callback_query(F.data == "done_tags", OfferService.service_type)
async def process_done_tags(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    selected_tags = user_data.get('selected_tags', [])
    custom_tags = user_data.get('custom_tags', [])
    all_tags = selected_tags + custom_tags

    if not all_tags:
        await callback.answer("Выберите хотя бы один тег", show_alert=True)
        return

    await state.update_data(service_type=all_tags)
    await callback.message.edit_text(
        f"Выбранные теги: {', '.join(all_tags)}\n{text.work_experience}",
        reply_markup=None
    )
    await state.set_state(OfferService.experience)
    await callback.answer()

async def update_tags_message(update: Union[Message, CallbackQuery], state: FSMContext):
    user_data = await state.get_data()
    selected_tags = user_data.get('selected_tags', [])
    custom_tags = user_data.get('custom_tags', [])
    total_tags = len(selected_tags) + len(custom_tags)
    existing_tags = await offer_keyboards.get_existing_tags()
    keyboard = offer_keyboards.get_tags_keyboard(existing_tags, selected_tags, True)
    text_lines = [
        f"Выбрано тегов: {total_tags}/3",
        "Стандартные: " + (', '.join(selected_tags) if selected_tags else "нет"),
        "Свои: " + (', '.join(custom_tags) if custom_tags else "нет"),
        "Выберите теги или введите свои:"
    ]

    if isinstance(update, CallbackQuery):
        await update.message.edit_text("\n".join(text_lines), reply_markup=keyboard)
    else:
        await update.answer("\n".join(text_lines), reply_markup=keyboard)

@router.message(OfferService.experience)
async def process_experience(message: Message, state: FSMContext):
    try:
        experience = int(message.text)
        if experience < 0 or experience > 70:
            await message.answer(text.real_experience)
            return
            
        await state.update_data(experience=experience)
        await message.answer(text.service_description)
        await state.set_state(OfferService.description)
    except ValueError:
        await message.answer(text.integer_experience)

@router.message(OfferService.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    user_data = await state.get_data()
    
    try:
        await save_to_db({
            'telegram_id': message.from_user.id,
            'telegram_nick': user_data['telegram_nick'],
            'phone': user_data['phone'],
            'full_name': user_data['full_name'],
            'service_type': user_data['service_type'],
            'experience': user_data['experience'],
            'description': user_data['description']
        })
        await message.answer(text.service_added)
    except KeyError as e:
        await message.answer(f'Ошибка: отсутствует обязательное поле {e}')
    finally:
        await state.clear()