from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    body: str
    commentable_object_type: str
    commentable_object_id: int


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    created: datetime

    class Config:
        orm_mode = True
