from CodewarsTelegramBot.database.db import engine
from CodewarsTelegramBot.database.models import User, Langs
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

async_session = async_sessionmaker(engine)  # Асинхронная сессия


async def set_user(user_id: int):
    async with async_session() as session:
        user = User(id=user_id)
        session.add(user)
        await session.commit()


async def set_lang(user_id: int, lang: Langs):
    if not await check_user(user_id):
        await set_user(user_id)
    async with async_session() as session:
        session.add(lang)
        await session.commit()


async def check_user(user_id: int) -> bool:
    async with async_session() as session:
        user = select(User).where(User.id == user_id)
        if await session.scalar(user) is None:
            return False
        else:
            return True


async def get_langs(user_id: int) -> list[Langs] | Langs:
    async with async_session() as session:
        langs = select(Langs).where(Langs.owner_id == user_id)
        langs = await session.execute(langs)
        return [it[0] for it in langs]


async def del_lang_query(user_id: int, lang: str):
    async with async_session() as session:
        stmt = select(Langs).where(Langs.lang == lang, Langs.owner_id == user_id)
        lang = await session.scalar(stmt)
        await session.delete(lang)
        await session.commit()

