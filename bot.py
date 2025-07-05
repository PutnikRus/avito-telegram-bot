import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Бот работает. Все сообщения с Авито будут приходить сюда.")

@dp.message(F.text)
async def handle_message(msg: Message):
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"""<b>Новое сообщение от:</b> {msg.from_user.full_name}
{msg.text}""",
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Ответить", callback_data=f"reply_{msg.from_user.id}")]
        ])
    )

if _name_ == "_main_":
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)
   
