from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from blog.models import Entry as EntryModel
from blog.repositories import EntryRepository
from blog.schemas import Entry as EntrySchema
from blog.schemas import EntryCreate as EntryCreateSchema


router = APIRouter()


@router.get("/", response_model=List[EntrySchema])
async def get_entries(
    offset: int = 0, entry_repository: EntryRepository = Depends(EntryRepository.instance)
) -> List[EntryModel]:
    return entry_repository.all(offset=offset)


@router.post("/", response_model=EntrySchema)
async def create_entry(
    entry: EntryCreateSchema,
    entry_repository: EntryRepository = Depends(EntryRepository.instance),
) -> EntryModel:
    try:
        return entry_repository.create(entry)
    except IntegrityError as cause:
        raise HTTPException(status_code=409, detail=str(cause.orig))


@router.get("/{entry_id}/", response_model=EntrySchema)
async def get_entry(
    entry_id: int, entry_repository: EntryRepository = Depends(EntryRepository.instance)
) -> EntryModel:
    return entry_repository.find_by_id(identifier=entry_id)
