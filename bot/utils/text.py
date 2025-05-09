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