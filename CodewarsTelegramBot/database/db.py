from CodewarsTelegramBot import get_db_conf
from sqlalchemy.ext.asyncio import create_async_engine

conf = get_db_conf()

user = conf["DB_USER"]
password = conf["DB_PASSWORD"]
host = conf["DB_HOST"]

engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@{host}/CodewarsBot")


