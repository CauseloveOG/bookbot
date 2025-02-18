import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import load_config, Config
from handlers import other_handlers, user_handlers
from keyboards.main_menu import set_main_menu


# Инициализация логгера
logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main():
    # Конфигруирование логгирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Вывод в консоль информации о запуске бота
    logging.info('Starting bot')

    # Загрузка конфиг в переменную config
    config: Config = load_config()

    # Инициализация бота и диспетчера
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Главное меню бота
    await set_main_menu(bot)

    # Регистрация роутеров в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропуск накопившихся апдейтов и запуск polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())