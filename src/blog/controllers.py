from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from blog.models import Entry as EntryModel
from blog.repositories import EntryRepository
from blog.schemas import Entry as EntrySchema
from blog.schemas import EntryCreate as EntryCreateSchema
from blog.schemas import EntryUpdate as EntryUpdateSchema


router = APIRouter()


@router.get("/", response_model=List[EntrySchema])
async def get_entries(
    offset: int = 0, entry_repository: EntryRepository = Depends(EntryRepository.instance)
) -> List[EntryModel]:
    """
    Retrieve entries.
    """
    return entry_repository.all(offset=offset)


@router.post("/", response_model=EntrySchema)
async def create_entry(
    entry: EntryCreateSchema,
    entry_repository: EntryRepository = Depends(EntryRepository.instance),
) -> EntryModel:
    """
    Create new entry.
    """
    try:
        return entry_repository.create(entry)
    except IntegrityError as cause:
        raise HTTPException(status_code=409, detail=str(cause.orig))


@router.put("/{entry_id}/", response_model=EntrySchema)
async def update_entry(
    entry_id: int,
    entry: EntryUpdateSchema,
    entry_repository: EntryRepository = Depends(EntryRepository.instance),
) -> EntryModel:
    entry_object = entry_repository.find_by_id(identifier=entry_id)
    if not entry_object:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry_repository.update(entry_object, entry)


@router.get("/{entry_id}/", response_model=EntrySchema)
async def get_entry(
    entry_id: int, entry_repository: EntryRepository = Depends(EntryRepository.instance)
) -> EntryModel:
    """
    Get entry by ID.
    """
    return entry_repository.find_by_id(identifier=entry_id)


@router.delete("/{entry_id}", response_model=EntrySchema)
def delete_item(
    entry_id: int, entry_repository: EntryRepository = Depends(EntryRepository.instance)
) -> EntryModel:
    """
    Delete an entry.
    """
    entry_object = entry_repository.find_by_id(identifier=entry_id)
    if not entry_object:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry_repository.remove(entry_object)
