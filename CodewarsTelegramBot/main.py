from CodewarsTelegramBot import dp, set_commands, AddLangStatesGroup, SettingsRouterStatesGroup
from CodewarsTelegramBot.database.query import check_user, get_langs, set_lang
from CodewarsTelegramBot.database.models import Langs
from CodewarsTelegramBot.keyboards import settings_keyboard, langs_keyboard, langs_priority_keyboards
from CodewarsTelegramBot.conf.CONSTANCE import STRINGS, DESCRIPTION
from CodewarsTelegramBot.random_kata import random_kata
from aiogram import executor
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from functools import wraps


def cancel_option(fun):
    """
    Обертка для сброса состояние при нажатии кнопки назад
    """
    @wraps(fun)
    async def wrapped_fun(message: Message, state: FSMContext, *args, **kwargs):
        if message.text == STRINGS.cancel:
            await state.reset_state()
            await message.answer("Возврат")
            return None
        return await fun(message, state, *args, **kwargs)
    return wrapped_fun


@dp.message_handler(commands=["kata"])
async def kata(message: Message):
    """
    Получить рандомную КАТА,
    если пользователя нет в БД предложить добавить языки
    """
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
    """
    Обработка команды настройки, предоставить меню настроек (клавиатуру),
    включить состояние ожидания этих настроек
    """
    await message.answer("Настройки", reply_markup=settings_keyboard())
    await SettingsRouterStatesGroup.router.set()


@dp.message_handler(commands=["help"])
async def help_descr(message: Message):
    """
    Обработка хелп, дать краткое описание
    """
    await message.answer(DESCRIPTION)


@dp.message_handler(content_types=["text"], state=SettingsRouterStatesGroup.router)
async def settings_router(message: Message, state: FSMContext):
    """
    Маршрутизатор настроек, ловится только если включено состояние ожидания выбора пути настроек
    """
    await state.reset_state()
    match message.text:
        case STRINGS.add_lang:
            await message.answer("Выберите язык", reply_markup=langs_keyboard())
            await AddLangStatesGroup.add_lang.set()
        case STRINGS.del_lang:
            await message.answer("Будем удалять язык")


@dp.message_handler(content_types=["text"], state=AddLangStatesGroup.add_lang)
@cancel_option
async def add_lang_lang(message: Message, state: FSMContext):
    """
    Состояние добавление языка в БД, принимаем название языка
    """
    async with state.proxy() as data:
        data["lang"] = message.text
    await message.answer("Выберите приоритет", reply_markup=langs_priority_keyboards())
    await AddLangStatesGroup.next()


@dp.message_handler(content_types=["text"], state=AddLangStatesGroup.add_priority)
@cancel_option
async def add_lang_priority(message: Message, state: FSMContext):
    """
    Состояние добавление языка в БД, принимаем приоритет
    """
    async with state.proxy() as data:
        data["priority"] = message.text
    await message.answer("Введите максимальную сложность (от 8 до 1)")
    await AddLangStatesGroup.next()


@dp.message_handler(content_types=["text"], state=AddLangStatesGroup.add_complexity_max)
@cancel_option
async def add_lang_max_complexity(message: Message, state: FSMContext):
    """
    Состояние добавление языка в БД, принимаем мах сложность
    """
    async with state.proxy() as data:
        data["max_c"] = message.text
    await message.answer("Введите минимальную сложность (от 8 до 1)")
    await AddLangStatesGroup.next()


@dp.message_handler(content_types=["text"], state=AddLangStatesGroup.add_complexity_min)
@cancel_option
async def add_lang_min_complexity(message: Message, state: FSMContext):
    """
    Состояние добавление языка в БД, принимаем мин сложность, добавляем в БД, сбрасываем состояние
    """
    async with state.proxy() as data:
        data["min_c"] = message.text
        await set_lang(message.from_user.id, Langs(owner_id=message.from_user.id,
                                                   lang=data["lang"],
                                                   lang_max=int(data["max_c"]),
                                                   lang_min=int(data["min_c"]),
                                                   lang_priority=data["priority"]))
        await message.answer("Готово")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=set_commands)
