start_text = 'Привет👋 Выбери действие ⬇️'
personal_data = 'Для публикации услуги нам потребуются твои данные. Дать согласие на их обработку?'
yes = '✅ Да'
no = '❌ Нет'
tg_nick = 'Введи свой ник в Telegram ⬇️'
data_needed = 'Для публикации услуги необходимо согласие на обработку данных'
send_phone = '📱 Отправить телефон'
find_service = '🔍 Найти услугу'
offer_service = '💼 Предложить услугу'
share_phone = 'Поделись номером телефона'
full_name = 'Введи своё имя и фамилию'
base_tags = ['Английский', 'Картины', 'Строительство']
tag_text = (
    "Выбери тип услуги:\n\n"
    "Можешь выбрать из популярных тегов ниже\n"
    "Или введи до 3 своих тегов через запятую\n"
)
work_experience = 'Укажи свой опыт работы в годах ⬇️'
real_experience = 'Пожалуйста, введи реальное количество лет опыта (0-70)'
integer_experience = 'Нужно ввести целое число'
choose_3_tags = 'Выберите до 3 тегов или введите свои:'
only_3_tags = 'Введите свой тег (или несколько через запятую):'
only_3_tags2 = 'Можно выбрать не более 3 тегов'
empty_tag = 'Выберите хотя бы один тег'
no_more_tags = 'Уже выбрано максимальное количество тегов'
chosen_tags = 'Выбранные теги:'
service_description = 'Добавь краткое описание своей услуги ⬇️'
service_added = 'Спасибо! Анкета добавлена ✅'
add_tag = '✏️ Ввести свой тег'
choose_tag = 'Выберите тег'
previous = '⬅️ Предыдущее'
next = 'Следующее ➡️'
no_offers = 'Нет предложений по этому тегу'
tag_error = 'Ошибка при обработке тега'
offer_upload_failed = 'Не удалось загрузить предложения'
session_expired = 'Сессия поиска истекла'
nav_error = 'Ошибка при навигации'
enter_custom_tag = 'Введите свой тег для поиска услуг ➡️'
no_offers_for_custom_tag = 'По вашему тегу не найдено предложений'
contact_admin = '📨 Написать админу'
support_text = 'Нажмите кнопку ниже для перехода в чат с администратором ⬇️'
no_active_offers = 'У Вас пока нет активных объявлений'
offers_error = 'Произошла ошибка при загрузке Ваших объявлений'

def get_tag_chosen_text(selected_tag: str) -> str:
    return f"Выбран тег: {selected_tag}"

def get_tags_experience_text(selected_tags: str) -> str:
    return f'Выбраны теги: {selected_tags}\nТеперь укажи свой опыт работы в годах ⬇️'

def get_tags_limit_text(available_slots: int) -> str:
    """Генерирует текст о лимите тегов с правильным склонением"""
    if available_slots == 1:
        return 'Можно добавить только 1 тег'
    return f'Можно добавить только {available_slots} тега'

def get_tags_selection_text(selected_tags: list, custom_tags: list) -> str:
    total = len(selected_tags) + len(custom_tags)
    selected_text = ', '.join(selected_tags) if selected_tags else "нет"
    custom_text = ', '.join(custom_tags) if custom_tags else "нет"
    
    return (
        f"Выбрано тегов: {total}/3\n"
        f"Стандартные: {selected_text}\n"
        f"Свои: {custom_text}\n"
        "Выберите теги или введите свои:"
    )

def format_offer(tag: str, offer: dict) -> str:
    """Форматирует текст предложения услуги"""
    telegram_nick = offer.get('telegram_nick')
    formatted_telegram = ''
    
    if telegram_nick:
        telegram_nick = telegram_nick.lstrip('@')
        formatted_telegram = f'@{telegram_nick}' if telegram_nick else 'Не указан'
    else:
        formatted_telegram = 'Не указан'

    return (
        f'🔹 Услуга: {tag}\n'
        f'👤 Исполнитель: {offer.get("full_name", "Не указан")}\n'
        f'📞 Телефон: {offer.get("phone", "Не указан")}\n'
        f'📱 Telegram: {formatted_telegram}\n'
        f'💼 Опыт: {offer.get("experience", "Не указан")}\n'
        f'📝 Описание: {offer.get("description", "Нет описания")}'
    )


def format_own_offer(offer: dict) -> str:
    """Форматирует текст объявления услуги при получении своих объявлений"""
    return (
        f'🔹 Теги: {offer.get("service_type")}\n'
        f'👤 Исполнитель: {offer.get("full_name", "Не указан")}\n'
        f'📞 Телефон: {offer.get("phone", "Не указан")}\n'
        f'📱 Telegram: {offer.get("telegram_nick", "Не указан")}\n'
        f'💼 Опыт: {offer.get("experience", "Не указан")}\n'
        f'📝 Описание: {offer.get("description", "Нет описания")}'
    )
