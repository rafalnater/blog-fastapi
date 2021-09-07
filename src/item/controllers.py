from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from item.models import Item as ItemModel
from item.repositories import ItemRepository
from item.schemas import Item as ItemSchema
from item.schemas import ItemCreate as ItemCreateSchema


router = APIRouter()


@router.get("/", response_model=List[ItemSchema])
async def get_items(
    offset: int = 0, item_repository: ItemRepository = Depends(ItemRepository.instance)
) -> List[ItemModel]:
    return item_repository.all(offset=offset)


@router.post("/", response_model=ItemSchema)
async def create_item(
    item: ItemCreateSchema,
    item_repository: ItemRepository = Depends(ItemRepository.instance),
) -> ItemModel:
    try:
        return item_repository.create(item)
    except IntegrityError as cause:
        raise HTTPException(status_code=409, detail=str(cause.orig))


@router.get("/{item_id}/", response_model=ItemSchema)
async def get_item(
    item_id: int, item_repository: ItemRepository = Depends(ItemRepository.instance)
) -> ItemModel:
    return item_repository.find_by_id(identifier=item_id)
