from core.mapper import AbstractMapper
from item.models import Item as ItemModel
from item.schemas import ItemCreate as ItemCreateSchema


class ItemCreationMapper(AbstractMapper[ItemCreateSchema, ItemModel]):
    @staticmethod
    def schema_to_model(schema: ItemCreateSchema) -> ItemModel:
        return ItemModel(
            title=schema.title,
            description=schema.description,
            owner_id=schema.owner_id,
        )
