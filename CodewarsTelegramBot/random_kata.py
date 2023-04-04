from CodewarsTelegramBot.conf import CONSTANCE
from CodewarsTelegramBot.database.models import Langs


def random_kata(langs_obj: list[Langs] | Langs) -> dict[str, int]:
    pass  # TODO Сергей. Функция маршрутизатор, Поэтапно вызывает все функции и
    # возвращает результат функции create_random_kata.


def create_lang_dict(langs_obj: list[Langs] | Langs) -> dict[str, list]:
    pass  # TODO Сергей


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
    те у которых приоритет выше, попадут в список больше раз
    и соответственно с большей вероятностью выпадут пользователю.\n
    "Normal", "High", "Very High" - варианты приоритетов
    :param langs: Словарь вида {Язык: {приоритет, min, max}, ...}
    :return: Список вида [Язык1, Язык1, Язык2]
    """
    lang_list = []
    for k, v in langs.items():
        iterations = 1
        match v["priority"]:
            case CONSTANCE.NORMAL:
                pass
            case CONSTANCE.HIGH:
                iterations = 2
            case CONSTANCE.VERY_HIGH:
                iterations = 3
        for i in range(iterations):
            lang_list.append(k)
    return lang_list


def create_random_kata(langs: list, langs_levels: dict[str, list]) -> dict[str, int]:
    pass  # TODO Сергей. Вернуть словарь вида {"lang": "Python", "level": 6}. См. тесты
