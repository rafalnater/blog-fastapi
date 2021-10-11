from datetime import datetime
from typing import Type

from fastapi.encoders import jsonable_encoder

from articles.mappers import ArticleCreationMapper
from articles.models import Article as ArticleModel
from articles.schemas import Article as ArticleSchema
from core.db import Base
from core.mapper import AbstractMapper
from core.repository import AbstractRepository, ModelType


class ArticleRepository(AbstractRepository[ArticleModel, int, ArticleSchema]):
    def _get_model_class(self) -> Type[Base]:
        return ArticleModel

    def _get_mapper(self) -> Type[AbstractMapper]:
        return ArticleCreationMapper

    def remove(self, article: ArticleModel) -> ArticleModel:
        self._db.delete(article)
        self._db.commit()
        return article

    def update(self, article: ArticleModel, update_data: ArticleSchema) -> ArticleModel:
        article_data = jsonable_encoder(article)
        if not isinstance(update_data, dict):
            update_data = update_data.dict(exclude_unset=True)

        for field in article_data:
            if field in update_data:
                setattr(article, field, update_data[field])
        article.modified = datetime.now()
        self._db.add(article)
        self._db.commit()
        self._db.refresh(article)
        return article
