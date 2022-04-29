from datetime import datetime

from core.mapper import AbstractMapper
from comments.models import Comment as CommentModel
from comments.schemas import CommentCreate as CommentCreateSchema


class CommentCreationMapper(AbstractMapper[CommentCreateSchema, CommentModel]):
    @staticmethod
    def schema_to_model(schema: CommentCreateSchema) -> CommentModel:
        return CommentModel(
            body=schema.body,
            created=datetime.now(),
        )
