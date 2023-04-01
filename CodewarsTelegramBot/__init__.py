from os import getenv
from telebot import TeleBot
from telebot.types import BotCommand

_TOKEN = getenv("TOKEN")

bot = TeleBot(_TOKEN)

bot.set_my_commands([BotCommand("/kata", "Выбрать задачу"),
                     BotCommand("/settings", "Настройки")])

print(f"Бот {bot} успешно создан")


