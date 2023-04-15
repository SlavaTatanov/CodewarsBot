from os import getenv
from sqlalchemy.ext.asyncio import create_async_engine

user = getenv("DB_USER")
password = getenv("DB_PASSWORD")
host = getenv("DB_HOST")

engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@{host}/CodewarsBot")


