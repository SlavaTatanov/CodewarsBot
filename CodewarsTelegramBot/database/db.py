from os import getenv
from sqlalchemy import create_engine

user = getenv("DB_USER")
password = getenv("DB_PASSWORD")
host = getenv("DB_HOST")

engine = create_engine(f"postgresql://{user}:{password}@{host}/CodewarsBot")


