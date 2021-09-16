from datetime import datetime

from core.mapper import AbstractMapper
from articles.models import Article as ArticleModel
from articles.schemas import ArticleCreate as ArticleCreateSchema


class ArticleCreationMapper(AbstractMapper[ArticleCreateSchema, ArticleModel]):
    @staticmethod
    def schema_to_model(schema: ArticleCreateSchema) -> ArticleModel:
        return ArticleModel(
            title=schema.title,
            body=schema.body,
            created=datetime.now(),
            modified=datetime.now(),
            pub_date=schema.pub_date,
            comments_count=schema.comments_count,
        )
