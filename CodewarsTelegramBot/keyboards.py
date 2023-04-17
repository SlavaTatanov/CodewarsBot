from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from CodewarsTelegramBot.conf.CONSTANCE import STRINGS, PRIORITY


def settings_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    for btn in (STRINGS.add_lang, STRINGS.del_lang, STRINGS.my_langs, STRINGS.cancel):
        keyboard.add(KeyboardButton(btn))
    return keyboard


def langs_keyboard(langs: list[str] = None):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    if langs:
        for lang in langs:
            keyboard.add(KeyboardButton(lang))
    keyboard.add(KeyboardButton(STRINGS.cancel))
    return keyboard


def langs_priority_keyboards():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    for it in [PRIORITY.NORMAL, PRIORITY.HIGH, PRIORITY.VERY_HIGH]:
        keyboard.add(KeyboardButton(it))
    keyboard.add(KeyboardButton(STRINGS.cancel))
    return keyboard


def submit_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    keyboard.add(KeyboardButton(STRINGS.yes))
    keyboard.add(KeyboardButton(STRINGS.no))
    return keyboard
