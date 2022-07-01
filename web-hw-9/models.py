from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()

# таблица для связи many-to-many между таблицами notes и tags
note_m2m_tag = Table(
    "note_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("note", Integer, ForeignKey("notes.id")),
    Column("tag", Integer, ForeignKey("tags.id")),
)

# Таблица notes, где будут храниться названия списка дел
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now())
    records = relationship("Record", cascade="all, delete", backref="note")
    tags = relationship("Tag", secondary=note_m2m_tag, backref="notes")

# Таблица records, где будут храниться записи для конкретного дела из таблицы notes - связь one-to-one, поле note_id
class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    description = Column(String(150), nullable=False)
    done = Column(Boolean, default=False)
    note_id = Column(Integer, ForeignKey(Note.id, ondelete="CASCADE"))

# Таблица tags, где хранится набор тегов для списка дел.
class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)