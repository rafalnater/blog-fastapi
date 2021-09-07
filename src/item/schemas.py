from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str = ""
    owner_id: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
