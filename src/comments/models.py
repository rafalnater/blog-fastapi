from sqlalchemy import Column, DateTime, Integer, Text, Unicode
from sqlalchemy_utils import generic_relationship

from core.db import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text)
    created = Column(DateTime)

    commentable_object_type = Column(Unicode(255))
    commentable_object_id = Column(Integer)
    commentable_object = generic_relationship(
        commentable_object_type,
        commentable_object_id,
    )
