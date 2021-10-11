from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EntryBase(BaseModel):
    title: Optional[str]
    body: str = ""
    comments_count: int = 0
    pub_date: Optional[datetime] = None


class EntryCreate(EntryBase):
    title: str


class EntryUpdate(EntryBase):
    pass


class Entry(EntryBase):
    id: int
    created: datetime
    modified: datetime

    class Config:
        orm_mode = True
