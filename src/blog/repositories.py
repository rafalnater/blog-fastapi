from typing import Type

from core.db import Base
from core.mapper import AbstractMapper
from core.repository import AbstractRepository, ModelType
from blog.mappers import EntryCreationMapper
from blog.models import Entry as EntryModel
from blog.schemas import Entry as EntrySchema


class EntryRepository(AbstractRepository[EntryModel, int, EntrySchema]):
    def _get_model_class(self) -> Type[Base]:
        return EntryModel

    def _get_mapper(self) -> Type[AbstractMapper]:
        return EntryCreationMapper

    def remove(self, entry: EntryModel) -> ModelType:
        # obj = self.find_by_id(id)
        self._db.delete(entry)
        self._db.commit()
        return entry

