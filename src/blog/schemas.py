from pydantic import BaseModel
from datetime import datetime


class EntryBase(BaseModel):
    title: str
    body: str = ""
    comments_count: int
    pub_date: datetime = None


class EntryCreate(EntryBase):
    pass


class Entry(EntryBase):
    id: int
    created: datetime
    modified: datetime

    class Config:
        orm_mode = True
