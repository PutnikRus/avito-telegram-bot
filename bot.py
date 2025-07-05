mport asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Имитация получения новых сообщений с Авито
def get_new_avito_messages():
    return [
        {
            "id": "msg_001",
            "sender": "Покупатель Иван",
            "text": "Здравствуйте, товар актуален?",
        }
    ]

# Обработка нажатия на кнопку "Ответить"
@dp.callback_query(lambda c: c.data.startswith("reply_"))
async def handle_reply_button(callback_query: types.CallbackQuery):
    message_id = callback_query.data.split("_", 1)[1]
    await bot.send_message(callback_query.from_user.id, f"Введите ответ на сообщение {message_id}")
    await callback_query.answer()

# Отправка новых сообщений в Telegram
async def poll_avito_messages():
    while True:
        messages = get_new_avito_messages()
        for msg in messages:
            keyboard = InlineKeyboardBuilder()
            keyboard.button(
                text="✏️ Ответить",
                callback_data=f"reply_{msg['id']}"
            )
            await bot.send_message(
                TELEGRAM_CHAT_ID,
                text=f"<b>Новое сообщение от:</b> {msg['sender']}

{msg['text']}",
                reply_markup=keyboard.as_markup()
            )
        await asyncio.sleep(30)

async def main():
    asyncio.create_task(poll_avito_messages())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

