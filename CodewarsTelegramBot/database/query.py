from CodewarsTelegramBot.database.db import engine
from CodewarsTelegramBot.database.models import User, Langs
from sqlalchemy.orm import Session
from sqlalchemy import select


def set_user(user_id: int):
    print("Начало запроса")
    with Session(engine) as session:
        user = User(id=user_id)
        print("Объект создан")
        session.add(user)
        print("Объект добавлен")
        session.commit()
        print("Готово")


def check_user(user_id: int) -> bool:
    with Session(engine) as session:
        user = select(User).where(User.id == user_id)
        if session.scalar(user) is None:
            return False
        else:
            return True



