import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from avito_client import AvitoClient

load_dotenv()

bot = Bot(
    token=os.getenv("TELEGRAM_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()
avito = AvitoClient()

reply_mode = {}

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Бот работает ✅")

@dp.callback_query(F.data.startswith("reply_"))
async def handle_reply_button(callback: CallbackQuery):
    user_id = callback.from_user.id
    chat_id = callback.data.split("_", 1)[1]
    reply_mode[user_id] = chat_id
    await callback.message.answer("Введите сообщение для ответа:")

@dp.message()
async def handle_text(message: Message):
    user_id = message.from_user.id
    if user_id in reply_mode:
        chat_id = reply_mode.pop(user_id)
        avito.send_reply(chat_id, message.text)
        await message.answer("Ответ отправлен ✅")
    else:
        await message.answer("Чтобы ответить на сообщение, нажмите кнопку 'Ответить' под ним.")

async def check_new_messages():
    while True:
        messages = avito.get_new_messages()
        for msg in messages:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✏️ Ответить", callback_data=f"reply_{msg['chat_id']}")]
            ])
            await bot.send_message(
                chat_id=int(os.getenv("TELEGRAM_CHAT_ID")),
                text=f"<b>Новое сообщение от:</b> {msg['sender']}

{msg['text']}",
                reply_markup=keyboard
            )
        await asyncio.sleep(30)

async def main():
    asyncio.create_task(check_new_messages())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())