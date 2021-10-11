from datetime import datetime
from typing import Type

from fastapi.encoders import jsonable_encoder

from blog.mappers import EntryCreationMapper
from blog.models import Entry as EntryModel
from blog.schemas import Entry as EntrySchema
from core.db import Base
from core.mapper import AbstractMapper
from core.repository import AbstractRepository, ModelType


class EntryRepository(AbstractRepository[EntryModel, int, EntrySchema]):
    def _get_model_class(self) -> Type[Base]:
        return EntryModel

    def _get_mapper(self) -> Type[AbstractMapper]:
        return EntryCreationMapper

    def remove(self, entry: EntryModel) -> EntryModel:
        self._db.delete(entry)
        self._db.commit()
        return entry

    def update(self, entry: EntryModel, update_data: EntrySchema) -> EntryModel:
        entry_data = jsonable_encoder(entry)
        if not isinstance(update_data, dict):
            update_data = update_data.dict(exclude_unset=True)

        for field in entry_data:
            if field in update_data:
                setattr(entry, field, update_data[field])
        entry.modified = datetime.now()
        self._db.add(entry)
        self._db.commit()
        self._db.refresh(entry)
        return entry
