import json
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage


def get_token():
    with open("CodewarsTelegramBot/config.json", "r") as config:
        data = json.load(config)
        return data["TOKEN"]


def get_db_conf():
    with open("CodewarsTelegramBot/config.json", "r") as config:
        data = json.load(config)
        return data


storage = MemoryStorage()

_TOKEN = get_token()

bot = Bot(_TOKEN)
dp = Dispatcher(bot, storage=storage)


async def set_commands(disp: Dispatcher):
    await disp.bot.set_my_commands([BotCommand("kata", "Рандомная задача"),
                                    BotCommand("settings", "Настройки"),
                                    BotCommand("help", "Помощь")])


class AddLangStatesGroup(StatesGroup):
    add_lang = State()
    add_priority = State()
    add_complexity_max = State()
    add_complexity_min = State()


class DelLangState(StatesGroup):
    del_lang = State()
    submit = State()


class ChangeLangState(StatesGroup):
    lang = State()
    router = State()
    priority = State()
    complexity_min = State()
    complexity_max = State()


class SettingsRouterStatesGroup(StatesGroup):
    router = State()
