def get_lang_list(langs: dict):
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
            case "Normal":
                pass
            case "High":
                iterations = 2
            case "Very High":
                iterations = 3
        for i in range(iterations):
            lang_list.append(k)
    return lang_list
