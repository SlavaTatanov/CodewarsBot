from CodewarsTelegramBot import bot, dp, set_commands, AddLangStatesGroup, SettingsRouterStatesGroup
from CodewarsTelegramBot.database.query import check_user, get_langs, set_lang
from CodewarsTelegramBot.database.models import Langs
from CodewarsTelegramBot.keyboards import settings_keyboard, langs_keyboard, langs_priority_keyboards
from CodewarsTelegramBot.conf.CONSTANCE import PRIORITY, STRINGS, DESCRIPTION
from CodewarsTelegramBot.random_kata import random_kata
from aiogram import executor
from aiogram.types import Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=["kata"])
async def kata(message: Message):
    if not await check_user(message.from_user.id):
        await message.answer("У вас не добавлено ни одного языка, чтобы начать работу с ботом, "
                             "добавьте хотя бы один язык.\n/settings")
    else:
        langs = await get_langs(message.from_user.id)
        answ = ""
        for lng in langs:
            answ = answ + " " + lng.lang
        await message.answer(f"{answ}")


@dp.message_handler(commands=["settings"])
async def settings(message: Message):
    await message.answer("Настройки", reply_markup=settings_keyboard())
    await SettingsRouterStatesGroup.router.set()


@dp.message_handler(commands=["help"])
async def help_descr(message: Message):
    await message.answer(DESCRIPTION)


@dp.message_handler(content_types=["text"], state=SettingsRouterStatesGroup.router)
async def settings_router(message: Message, state: FSMContext):
    await state.reset_state()
    match message.text:
        case STRINGS.add_lang:
            await message.answer("Выберите язык", reply_markup=langs_keyboard())
            await AddLangStatesGroup.add_lang.set()
        case STRINGS.del_lang:
            await message.answer("Будем удалять язык")


@dp.message_handler(content_types=["text"], state=AddLangStatesGroup.add_lang)
async def add_lang_lang(message: Message, state: FSMContext):
    if message.text == STRINGS.cancel:
        await state.reset_state()
        await message.answer("Возврат")
    else:
        async with state.proxy() as data:
            data["lang"] = message.text
        await message.answer("Выберите приоритет", reply_markup=langs_priority_keyboards())
        await AddLangStatesGroup.next()


@dp.message_handler(content_types=["text"], state=AddLangStatesGroup.add_priority)
async def add_lang_priority(message: Message, state: FSMContext):
    if message.text == STRINGS.cancel:
        await state.reset_state()
        await message.answer("Возврат")
    else:
        async with state.proxy() as data:
            data["priority"] = message.text
        await message.answer("Введите максимальную сложность")
        await AddLangStatesGroup.next()


# def settings_router(message):
#     match message.text:
#         case STRINGS.str_add_lang:
#             bot.send_message(message.chat.id, "Выберете язык")
#             set_lang(message.chat.id, Langs(owner_id=message.chat.id,
#                                             lang="Java",
#                                             lang_min=8,
#                                             lang_max=4,
#                                             lang_priority=PRIORITY.NORMAL))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=set_commands)

