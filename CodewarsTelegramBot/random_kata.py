from CodewarsTelegramBot.conf import CONSTANCE


def get_lang_levels(langs: dict) -> dict:
    """
    Принимает словарь язык: мин, мах уровни.
    Возвращает словарь язык: [5, 6, 7]
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
    :param langs: Словарь вида {Язык: приоритет, ...}
    :return: Список вида [Язык1, Язык1, Язык2]
    """
    lang_list = []
    for k, v in langs.items():
        iterations = 1
        match v:
            case CONSTANCE.NORMAL:
                pass
            case CONSTANCE.HIGH:
                iterations = 2
            case CONSTANCE.VERY_HIGH:
                iterations = 3
        for i in range(iterations):
            lang_list.append(k)
    return lang_list
