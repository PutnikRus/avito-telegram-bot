import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import os

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Бот работает!")

# Заглушка под реальный функционал
async def main():
    from aiogram import executor
    from dotenv import load_dotenv
    load_dotenv()
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())