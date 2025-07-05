import logging
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

bot = Bot(token=TOKEN, default=types.DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# FSM для состояния "ожидаем текст ответа"
class ReplyState(StatesGroup):
    waiting_for_text = State()
    replying_to_user = State()

# Храним ID пользователя, которому нужно ответить
reply_targets = {}

@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Бот работает. Все сообщения с Авито будут приходить сюда.")

@dp.message(F.text)
async def handle_message(msg: Message):
    if msg.chat.id == ADMIN_CHAT_ID and msg.chat.id in reply_targets:
        # Админ отправляет ответ
        user_id = reply_targets.pop(msg.chat.id)
        await bot.send_message(user_id, msg.text)
        await msg.answer("✅ Ответ отправлен.")
    else:
        # Пользователь отправляет сообщение
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"<b>Новое сообщение от:</b> {msg.from_user.full_name}\n{msg.text}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Ответить", callback_data=f"reply_{msg.from_user.id}")]
            ])
        )

@dp.callback_query(F.data.startswith("reply_"))
async def handle_reply_button(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    reply_targets[callback.message.chat.id] = user_id
    await callback.message.answer("✍️ Введите текст ответа, и он будет отправлен пользователю.")
    await callback.answer()

if _name_ == "_main_":
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)
