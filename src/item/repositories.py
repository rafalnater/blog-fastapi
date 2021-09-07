from typing import Type

from core.db import Base
from core.mapper import AbstractMapper
from core.repository import AbstractRepository
from item.mappers import ItemCreationMapper
from item.models import Item as ItemModel
from item.schemas import Item as ItemSchema


class ItemRepository(AbstractRepository[ItemModel, int, ItemSchema]):
    def _get_model_class(self) -> Type[Base]:
        return ItemModel

    def _get_mapper(self) -> Type[AbstractMapper]:
        return ItemCreationMapper
