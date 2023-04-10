class ConstanceClassError(Exception):
    def __str__(self):
        return "Нельзя создать экземпляр из класса с константами"


class BaseConstance:
    """
    Базовый класс для констант, который запрещает создавать его экземпляры
    """
    def __init__(self):
        raise ConstanceClassError


class PRIORITY(BaseConstance):
    """
    Приоритеты языков
    """
    NORMAL = "Normal"
    HIGH = "High"
    VERY_HIGH = "Very High"


class STRINGS(BaseConstance):
    str_add_lang = "Добавить язык"

