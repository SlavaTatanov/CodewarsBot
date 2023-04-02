from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)


class Langs(Base):
    __tablename__ = "langs"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"),
                                          nullable=False)
    lang: Mapped[str]
    lang_min: Mapped[int]
    lang_max: Mapped[int]
    lang_priority: Mapped[str]

