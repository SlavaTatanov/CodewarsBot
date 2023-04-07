from CodewarsTelegramBot.database.db import engine
from CodewarsTelegramBot.database.models import User, Langs
from sqlalchemy.orm import Session
from sqlalchemy import select


def set_user(user_id: int):
    with Session(engine) as session:
        user = User(id=user_id)
        session.add(user)
        session.commit()


def set_lang(user_id: int, lang: Langs):
    if not check_user(user_id):
        set_user(user_id)
    with Session(engine) as session:
        session.add(lang)
        session.commit()


def check_user(user_id: int) -> bool:
    with Session(engine) as session:
        user = select(User).where(User.id == user_id)
        if session.scalar(user) is None:
            return False
        else:
            return True


def get_langs(user_id: int) -> list[Langs] | Langs:
    with Session(engine) as session:
        langs = select(Langs).where(Langs.owner_id == user_id)
        if langs is not None:
            langs = session.execute(langs).all()
            return [it[0] for it in langs]



