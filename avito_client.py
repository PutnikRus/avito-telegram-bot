import os
from dotenv import load_dotenv

load_dotenv()

class AvitoClient:
    def _init_(self):  # ✅ двойное подчёркивание
        self.login = os.getenv("AVITO_LOGIN")
        self.password = os.getenv("AVITO_PASSWORD")

    def get_new_messages(self):
        # Заглушка — просто тестовое сообщение
        return [{
            "chat_id": "123456",
            "sender": "Покупатель Иван",
            "text": "Здравствуйте, актуально?"
        }]

    def send_reply(self, chat_id, text):
        print(f"Отправляем ответ в чат {chat_id}: {text}")
