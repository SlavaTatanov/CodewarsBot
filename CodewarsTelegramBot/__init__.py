from os import getenv
from aiogram import Bot, Dispatcher

_TOKEN = getenv("TOKEN")

bot = Bot(_TOKEN)
dp = Dispatcher(bot)




