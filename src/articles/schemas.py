from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: Optional[str]
    body: str = ""
    comments_count: int = 0
    pub_date: Optional[datetime] = None


class ArticleCreate(ArticleBase):
    title: str


class ArticleUpdate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    created: datetime
    modified: datetime

    class Config:
        orm_mode = True
