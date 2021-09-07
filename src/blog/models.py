from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from core.db import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(Text)
    created = Column(DateTime)
    modified = Column(DateTime)
    pub_date = Column(DateTime)
    comments_count = Column(Integer)
