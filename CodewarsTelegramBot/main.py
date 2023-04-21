from CodewarsTelegramBot import dp, set_commands, AddLangStatesGroup, SettingsRouterStatesGroup, DelLangState, \
    ChangeLangState
from CodewarsTelegramBot.database.query import check_user, get_langs, set_lang, del_lang_query, update_lang_priority, \
    get_lang, update_lang_complexity
from CodewarsTelegramBot.database.models import Langs
from CodewarsTelegramBot.keyboards import settings_keyboard, langs_keyboard, langs_priority_keyboards, submit_keyboard, \
    complexity_keyboard, change_lang_keyboard
from CodewarsTelegramBot.conf.CONSTANCE import STRINGS, DESCRIPTION, PRIORITY
from CodewarsTelegramBot.random_kata import random_kata
from aiogram import executor
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from functools import wraps


def cancel_option(fun):
    """
    Обертка для сброса состояния при нажатии кнопки назад
    """
    @wraps(fun)
    async def wrapped_fun(message: Message, state: FSMContext):
        if message.text == STRINGS.cancel:
            await state.reset_state()
            await message.answer("Возврат")
            return None
        return await fun(message, state)
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
        answer = random_kata(langs)
        await message.answer(f"Язык {answer['lang']}. Сложность - {answer['level']}")


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
            langs = await get_langs(message.from_user.id)
            langs = [obj.lang for obj in langs]
            keyboard = langs_keyboard(langs)
            await message.answer("Выберете язык", reply_markup=keyboard)
            await DelLangState.del_lang.set()
        case STRINGS.my_langs:
            langs = await get_langs(message.from_user.id)
            langs = [obj.lang for obj in langs]
            keyboard = langs_keyboard(langs)
            await message.answer("Какой язык необходимо изменить?", reply_markup=keyboard)
            await ChangeLangState.lang.set()


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
    await message.answer("Введите максимальную сложность (от 8 до 1)", reply_markup=complexity_keyboard())
    await AddLangStatesGroup.next()


@dp.message_handler(content_types=["text"], state=AddLangStatesGroup.add_complexity_max)
@cancel_option
async def add_lang_max_complexity(message: Message, state: FSMContext):
    """
    Состояние добавление языка в БД, принимаем мах сложность
    """
    async with state.proxy() as data:
        data["max_c"] = message.text
    await message.answer("Введите минимальную сложность (от 8 до 1)", reply_markup=complexity_keyboard())
    await AddLangStatesGroup.next()


@dp.message_handler(content_types=["text"], state=AddLangStatesGroup.add_complexity_min)
@cancel_option
async def add_lang_min_complexity(message: Message, state: FSMContext):
    """
    Состояние добавление языка в БД, принимаем мин сложность, добавляем в БД, сбрасываем состояние
    """
    async with state.proxy() as data:
        data["min_c"] = message.text
        complexity = [int(data["max_c"]), int(data["min_c"])]
        complexity.sort()
        await set_lang(message.from_user.id, Langs(owner_id=message.from_user.id,
                                                   lang=data["lang"],
                                                   lang_max=complexity[0],
                                                   lang_min=complexity[1],
                                                   lang_priority=data["priority"]))
        await message.answer("Готово")
    await state.finish()


@dp.message_handler(content_types=["text"], state=DelLangState.del_lang)
@cancel_option
async def del_lang(message: Message, state: FSMContext):
    """
    Удаление языки, принимаем язык с клавиатуры
    """
    async with state.proxy() as data:
        data["lang"] = message.text
    await message.answer(f"Вы точно хотите удалить {data['lang']}?", reply_markup=submit_keyboard())
    await DelLangState.next()


@dp.message_handler(content_types=["text"], state=DelLangState.submit)
@cancel_option
async def del_lang_submit(message: Message, state: FSMContext):
    """
    Финальный запрос у пользователя, что он уверен в удаление языка
    """
    if message.text == STRINGS.no:
        await state.reset_state()
        await message.answer("Отмена")
    if message.text == STRINGS.yes:
        async with state.proxy() as data:
            lang = data["lang"]
            await del_lang_query(message.from_user.id, lang)
            await message.answer("Успешно")
            await state.finish()


@dp.message_handler(content_types=["text"], state=ChangeLangState.lang)
@cancel_option
async def change_lang(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["lang"] = message.text
        lang = await get_lang(message.from_user.id, message.text)
        await message.answer(f"Язык {lang.lang}\n"
                             f"Приоритет - {lang.lang_priority}\n"
                             f"Минимальная сложность - {lang.lang_min}\n"
                             f"Максимальная сложность - {lang.lang_max}")
    await message.answer("Что необходимо изменить?", reply_markup=change_lang_keyboard())
    await ChangeLangState.next()


@dp.message_handler(content_types=["text"], state=ChangeLangState.router)
@cancel_option
async def change_lang_router(message: Message, state: FSMContext):
    match message.text:
        case STRINGS.priority:
            await message.answer("Выберете приоритет для языка", reply_markup=langs_priority_keyboards())
            await ChangeLangState.priority.set()
        case STRINGS.min_cap:
            await message.answer("Введите минимальную сложность", reply_markup=complexity_keyboard())
            await ChangeLangState.complexity_min.set()
        case STRINGS.max_cap:
            await message.answer("Введите максимальную сложность", reply_markup=complexity_keyboard())
            await ChangeLangState.complexity_max.set()


@dp.message_handler(content_types=["text"], state=ChangeLangState.priority)
@cancel_option
async def change_lang_priority(message: Message, state: FSMContext):
    if message.text in [PRIORITY.NORMAL, PRIORITY.HIGH, PRIORITY.VERY_HIGH]:
        async with state.proxy() as data:
            lang = data["lang"]
            await update_lang_priority(message.from_user.id, lang, message.text)
            await message.answer("Приоритет изменен")
        await state.reset_state()


@dp.message_handler(content_types=["text"], state=ChangeLangState.complexity_min)
@cancel_option
async def change_lang_complexity(message: Message, state: FSMContext):
    async with state.proxy() as data:
        lang = data["lang"]
        await update_lang_complexity(message.from_user.id, lang, int(message.text), "min")
        await message.answer("Выполнено")
        await state.finish()


@dp.message_handler(content_types=["text"], state=ChangeLangState.complexity_max)
@cancel_option
async def change_lang_complexity(message: Message, state: FSMContext):
    async with state.proxy() as data:
        lang = data["lang"]
        await update_lang_complexity(message.from_user.id, lang, int(message.text), "max")
        await message.answer("Выполнено")
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=set_commands)
