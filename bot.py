import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# ⛔ Проверка, чтобы токен точно был
if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN не задан в .env")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# 🧠 Храним, кому именно админ хочет ответить
current_replies = {}

# Команда /start
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("✅ Бот работает. Все сообщения с Авито будут приходить сюда.")

# Получение обычного текста от любого пользователя
@dp.message(F.text)
async def handle_message(msg: Message):
    # Сообщение админа — это ответ?
    if str(msg.chat.id) == str(ADMIN_CHAT_ID):
        user_id = current_replies.get(msg.from_user.id)
        if user_id:
            await bot.send_message(chat_id=user_id, text=msg.text)
            await msg.answer("✉️ Ответ отправлен.")
        else:
            await msg.answer("❌ Вы не выбрали, кому ответить.")
        return

    # Сообщение от обычного пользователя — пересылаем админу
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Ответить", callback_data=f"reply_{msg.from_user.id}"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_reply")
        ]
    ])
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"<b>Новое сообщение от:</b> {msg.from_user.full_name}\n\n{msg.text}",
        reply_markup=kb
    )

# Обработка фото от пользователей и админа
@dp.message(F.photo)
async def handle_photo(msg: Message):
    if str(msg.chat.id) == str(ADMIN_CHAT_ID):
        user_id = current_replies.get(msg.from_user.id)
        if user_id:
            await bot.send_photo(chat_id=user_id, photo=msg.photo[-1].file_id, caption=msg.caption)
            await msg.answer("📷 Фото отправлено.")
        else:
            await msg.answer("❌ Вы не выбрали, кому отправить фото.")
        return

    # Фото от обычного пользователя
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Ответить", callback_data=f"reply_{msg.from_user.id}"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_reply")
        ]
    ])
    await bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=msg.photo[-1].file_id,
        caption=f"<b>Новое фото от:</b> {msg.from_user.full_name}",
        reply_markup=kb
    )

# Обработка кнопки "Ответить"
@dp.callback_query(F.data.startswith("reply_"))
async def handle_reply(callback: CallbackQuery):
    target_user_id = int(callback.data.split("_")[1])
    current_replies[callback.from_user.id] = target_user_id
    await callback.message.answer("✏️ Введите сообщение, и я отправлю его пользователю.")
    await callback.answer()

# Обработка кнопки "Отменить"
@dp.callback_query(F.data == "cancel_reply")
async def cancel_reply(callback: CallbackQuery):
    current_replies.pop(callback.from_user.id, None)
    await callback.message.answer("❌ Ответ отменён.")
    await callback.answer()

# Точка входа
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)
