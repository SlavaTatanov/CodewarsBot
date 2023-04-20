import random

from CodewarsTelegramBot.conf.CONSTANCE import PRIORITY
from CodewarsTelegramBot.database.models import Langs


def random_kata(langs_obj: list[Langs] | Langs) -> dict[str, int]:
    """
    Функция-маршрутизатор. На вход принимает объект класса
    Langs. Поочерёдно вызывает все функции и возвращает
    результат функции create_random_kata
    param: langs_obj
    return: словарь вида {"lang": "Python", "level": 5}
    """
    lang_dict = create_lang_dict(langs_obj)
    lang_levels = get_lang_levels(lang_dict)
    lang_list = get_lang_list(lang_dict)
    return create_random_kata(lang_list, lang_levels)


def create_lang_dict(langs_obj: list[Langs] | Langs) -> dict[str, list]:
    """
    Функция принимает список объектов функции Langs.
    Формирует словарь вида {{"Python": {"min": 6, "max": 4, "priority": "Normal"}}}
    """
    lang_dict = {lang.lang: {'min': lang.lang_min, 'max': lang.lang_max,
                             'priority': lang.lang_priority} for lang in langs_obj}
    return lang_dict


def get_lang_levels(langs: dict) -> dict:
    """
    Принимает словарь язык: мин, мах уровни.
    Возвращает словарь {язык: [5, 6, 7]}
    """
    lang_levels = {}
    for key, val in langs.items():
        lang_levels[key] = list(range(val["max"], val["min"] + 1))
    return lang_levels


def get_lang_list(langs: dict) -> list:
    """
    Функция принимает словарь с приоритетами языков и создает список,
    который учитывает их приоритет,
    те у которых приоритет выше, попадут в список больше ра
    и соответственно с большей вероятностью выпадут пользователю.\n
    "Normal", "High", "Very High" - варианты приоритетов
    :param langs: Словарь вида {Язык: {приоритет, min, max}, ...}
    :return: Список вида [Язык1, Язык1, Язык2]
    """
    lang_list = []
    for k, v in langs.items():
        iterations = 1
        match v["priority"]:
            case PRIORITY.NORMAL:
                pass
            case PRIORITY.HIGH:
                iterations = 2
            case PRIORITY.VERY_HIGH:
                iterations = 3
        for i in range(iterations):
            lang_list.append(k)
    return lang_list


def create_random_kata(langs: list, langs_levels: dict[str, list]) -> dict[str, int]:
    """
    Функция принимает словарь со списком языков и словарь с
    уровнями сложности для каждого языка и создаёт словарь
    со случайно выбранным языком и уровнем сложности для него.
    :param langs: Список вида ["Python", "Haskel", "Java" ]
    :param langs_levels: Словарь вида {"Haskell": [6, 7, 8], "Python": [4, 5, 6, 7]}
    :return: Словарь вида {"lang": "Python", "level": 5}
    """
    created_kata = dict()
    created_kata["lang"] = random.choice(langs)
    if created_kata["lang"] in langs_levels.keys():
        created_kata["level"] = random.choice(langs_levels[created_kata["lang"]])
    return created_kata
