import os
from dotenv import load_dotenv

load_dotenv()

class AvitoClient:
    def __init__(self):
        self.login = os.getenv("AVITO_LOGIN")
        self.password = os.getenv("AVITO_PASSWORD")

    def get_new_messages(self):
        return [{
            "chat_id": "123456",
            "sender": "Покупатель Иван",
            "text": "Здравствуйте, актуально?"
        }]

    def send_reply(self, chat_id, text):
        print(f"Отправляем ответ в чат {chat_id}: {text}")