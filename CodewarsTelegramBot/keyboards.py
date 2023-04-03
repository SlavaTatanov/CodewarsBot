from telebot.types import ReplyKeyboardMarkup
from CodewarsTelegramBot.conf import CONSTANCE


def settings_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    for btn in (CONSTANCE.str_add_lang, "Удалить язык", "Мои языки", "Назад"):
        keyboard.add(btn)
    return keyboard
