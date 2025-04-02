from aiogram.fsm.state import State, StatesGroup


class OfferService(StatesGroup):
    confirm_data = State()
    telegram_nick = State()
    phone = State()
    full_name = State()
    service_type = State()
    custom_tag_input = State() 
    experience = State()
    description = State()