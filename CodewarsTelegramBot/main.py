from CodewarsTelegramBot import bot
from CodewarsTelegramBot.database.query import check_user, get_langs, set_lang
from CodewarsTelegramBot.database.models import Langs
from CodewarsTelegramBot.keyboards import settings_keyboard
from CodewarsTelegramBot.conf.CONSTANCE import PRIORITY, STRINGS
from CodewarsTelegramBot.random_kata import random_kata


@bot.message_handler(commands=["kata"])
def kata(message):
    if not check_user(message.chat.id):
        bot.send_message(message.chat.id, "У вас не добавлено ни одного языка, чтобы начать работу с ботом, добавьте"
                                          "хотя бы один язык.\n/settings")
    else:
        langs = get_langs(message.chat.id)
        # kata_for_user = random_kata(langs)


@bot.message_handler(commands=["settings"])
def settings(message):
    bot.send_message(message.chat.id, "Ваши настройки", reply_markup=settings_keyboard())
    bot.register_next_step_handler(message, settings_router)


def settings_router(message):
    match message.text:
        case STRINGS.str_add_lang:
            bot.send_message(message.chat.id, "Выберете язык")
            set_lang(message.chat.id, Langs(owner_id=message.chat.id,
                                            lang="Java",
                                            lang_min=8,
                                            lang_max=4,
                                            lang_priority=PRIORITY.NORMAL))


if __name__ == '__main__':
    bot.polling(none_stop=True)

