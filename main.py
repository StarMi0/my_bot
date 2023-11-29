import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher

import handlers.users

# Configure logging
logging.basicConfig(level=logging.INFO)

# Загружаем токен из переменной окружения
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# Проверяем, что токен был загружен
if not API_TOKEN:
    raise ValueError("No token provided.Set TELEGRAM_API_TOKEN environment variable.")

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")


async def main():
    # Регистрируем хэндлер cmd_test2 по команде /start
    dp.include_routers(handlers.users.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, mylist=[1, 2, 3])


if __name__ == "__main__":
    asyncio.run(main())
