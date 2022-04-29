from typing import Type, Union, List

from articles.models import Article
from blog.models import Entry
from core.db import Base
from core.mapper import AbstractMapper
from core.repository import AbstractRepository, ModelType
from comments.mappers import CommentCreationMapper
from comments.models import Comment as CommentModel
from comments.schemas import Comment as CommentSchema
from comments.schemas import CommentCreate as CommentCreateSchema


class CommentRepository(AbstractRepository[CommentModel, int, CommentSchema]):
    def _get_model_class(self) -> Type[Base]:
        return CommentModel

    def _get_mapper(self) -> Type[AbstractMapper]:
        return CommentCreationMapper

    def create_with_commentable_object(
        self,
        schema: CommentCreateSchema,
        commentable_object: Union[Entry, Article],
    ) -> ModelType:
        mapper = self._get_mapper()
        comment = mapper.schema_to_model(schema)
        comment.commentable_object = commentable_object

        self._db.add(comment)
        self._db.commit()
        self._db.refresh(comment)

        return comment

    def remove(self, comment: CommentModel) -> ModelType:
        self._db.delete(comment)
        self._db.commit()
        return comment

    def filter_by_commentable_object(
        self,
        commentable_object_type: str,
        commentable_object_id: int,
        offset: int = 0
    ) -> List[ModelType]:
        return (
            self._db.query(self._get_model_class())
            .filter_by(
                commentable_object_type=commentable_object_type,
                commentable_object_id=commentable_object_id,
            )
            .offset(offset)
            .limit(self._per_page)
            .all()
        )
