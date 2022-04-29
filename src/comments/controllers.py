from typing import List

from articles.repositories import ArticleRepository
from blog.repositories import EntryRepository
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from comments.models import Comment as CommentModel
from comments.repositories import CommentRepository
from comments.schemas import Comment as CommentSchema
from comments.schemas import CommentCreate as CommentCreateSchema


router = APIRouter()


@router.get("/", response_model=List[CommentSchema])
async def get_comments(
    commentable_object_type: str,
    commentable_object_id: int,
    offset: int = 0,
    comment_repository: CommentRepository = Depends(CommentRepository.instance)
) -> List[CommentModel]:
    """
    Retrieve comments.
    """
    return comment_repository.filter_by_commentable_object(
        commentable_object_type=commentable_object_type,
        commentable_object_id=commentable_object_id,
        offset=offset,
    )


@router.post("/", response_model=CommentSchema)
async def create_comment(
    comment: CommentCreateSchema,
    comment_repository: CommentRepository = Depends(CommentRepository.instance),
    entry_repository: EntryRepository = Depends(EntryRepository.instance),
    article_repository: ArticleRepository = Depends(ArticleRepository.instance),
) -> CommentModel:
    """
    Create new comment.
    """
    try:
        commentable_object_type = comment.commentable_object_type.lower()
        commentable_object_repositories = {
            'entry': entry_repository,
            'article': article_repository,
        }
        if commentable_object_type not in commentable_object_repositories.keys():
            raise HTTPException(status_code=400, detail=f"Invalid commentable object type")

        commentable_object_repository = commentable_object_repositories.get(
            commentable_object_type
        )
        commentable_object = commentable_object_repository.find_by_id(
            identifier=comment.commentable_object_id
        )

        if not commentable_object:
            raise HTTPException(status_code=400, detail=f"Commentable object not found")

        return comment_repository.create_with_commentable_object(
            comment,
            commentable_object,
        )
    except IntegrityError as cause:
        raise HTTPException(status_code=409, detail=str(cause.orig))


@router.delete("/{comment_id}", response_model=CommentSchema)
def delete_comment(
    comment_id: int,
    comment_repository: CommentRepository = Depends(CommentRepository.instance)
) -> CommentModel:
    """
    Delete a comment.
    """
    comment_object = comment_repository.find_by_id(identifier=comment_id)
    if not comment_object:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment_repository.remove(comment_object)
