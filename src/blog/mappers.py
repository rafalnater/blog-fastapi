from datetime import datetime

from blog.models import Entry as EntryModel
from blog.schemas import EntryCreate as EntryCreateSchema
from core.mapper import AbstractMapper


class EntryCreationMapper(AbstractMapper[EntryCreateSchema, EntryModel]):
    @staticmethod
    def schema_to_model(schema: EntryCreateSchema) -> EntryModel:
        return EntryModel(
            title=schema.title,
            body=schema.body,
            created=datetime.now(),
            modified=datetime.now(),
            pub_date=schema.pub_date,
            comments_count=schema.comments_count,
        )
