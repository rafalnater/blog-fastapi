from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from articles.models import Article as ArticleModel
from articles.repositories import ArticleRepository
from articles.schemas import Article as ArticleSchema
from articles.schemas import ArticleCreate as ArticleCreateSchema
from articles.schemas import ArticleUpdate as ArticleUpdateSchema


router = APIRouter()


@router.get("/", response_model=List[ArticleSchema])
async def get_articles(
    offset: int = 0, article_repository: ArticleRepository = Depends(ArticleRepository.instance)
) -> List[ArticleModel]:
    """
    Retrieve articles.
    """
    return article_repository.all(offset=offset)


@router.post("/", response_model=ArticleSchema)
async def create_article(
    article: ArticleCreateSchema,
    article_repository: ArticleRepository = Depends(ArticleRepository.instance),
) -> ArticleModel:
    """
    Create new article.
    """
    try:
        return article_repository.create(article)
    except IntegrityError as cause:
        raise HTTPException(status_code=409, detail=str(cause.orig))


@router.put("/{article_id}/", response_model=ArticleSchema)
async def update_article(
    article_id: int,
    article: ArticleUpdateSchema,
    article_repository: ArticleRepository = Depends(ArticleRepository.instance),
) -> ArticleModel:
    article_object = article_repository.find_by_id(identifier=article_id)
    if not article_object:
        raise HTTPException(status_code=404, detail="Article not found")
    return article_repository.update(article_object, article)


@router.get("/{article_id}/", response_model=ArticleSchema)
async def get_article(
    article_id: int, article_repository: ArticleRepository = Depends(ArticleRepository.instance)
) -> ArticleModel:
    """
    Get article by ID.
    """
    return article_repository.find_by_id(identifier=article_id)


@router.delete("/{article_id}", response_model=ArticleSchema)
def delete_item(
    article_id: int, article_repository: ArticleRepository = Depends(ArticleRepository.instance)
) -> ArticleModel:
    """
    Delete an article.
    """
    article_object = article_repository.find_by_id(identifier=article_id)
    if not article_object:
        raise HTTPException(status_code=404, detail="Article not found")
    return article_repository.remove(article_object)
