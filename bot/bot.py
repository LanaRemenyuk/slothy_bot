import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from dotenv import load_dotenv

from handlers.common import router

load_dotenv()

secret_token = os.getenv('TOKEN')

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация бота
async def setup_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Начало работы'),
        BotCommand(command='/help', description='Помощь'),
        BotCommand(command='/support', description='Связь с поддержкой'),
        BotCommand(command='/myoffers', description='Мои объявления')
    ]
    await bot.set_my_commands(commands)

async def on_startup(bot: Bot, dispatcher: Dispatcher):
    await setup_bot_commands(bot)
    logger.info('Бот запущен')

async def on_shutdown(bot: Bot, dispatcher: Dispatcher):
    logger.info('Бот остановлен')
    await bot.session.close()

async def main():

    # Инициализация бота
    bot = Bot(
        token=secret_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
    
    # Инициализация диспетчера с хранилищем состояний
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрация роутера 
    dp.include_router(router)

    # Подписка на события запуска/остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    try:
        await dp.start_polling(
            bot,
            handle_signals=True,
            allowed_updates=dp.resolve_used_update_types(),
            close_bot_session=True
        )
    except asyncio.CancelledError:
        logger.info('Поллинг остановлен')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Бот остановлен по запросу пользователя')
        