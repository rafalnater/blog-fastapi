from sqlalchemy import Column, DateTime, Integer, Text, Unicode
from sqlalchemy_utils import generic_relationship

from core.db import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text)
    created = Column(DateTime)

    object_type = Column(Unicode(255))
    object_id = Column(Integer)
    object = generic_relationship(object_type, object_id)
