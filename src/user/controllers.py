from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from user.models import User as UserModel
from user.repositories import UserRepository
from user.schemas import User as UserSchema
from user.schemas import UserCreate as UserCreateSchema


router = APIRouter()


@router.get("/", response_model=List[UserSchema])
async def get_users(
    offset: int = 0, user_repository: UserRepository = Depends(UserRepository.instance)
) -> List[UserModel]:
    return user_repository.all(offset=offset)


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreateSchema,
    user_repository: UserRepository = Depends(UserRepository.instance),
) -> UserModel:
    try:
        return user_repository.create(user)
    except IntegrityError as cause:
        raise HTTPException(status_code=409, detail=str(cause.orig))


@router.get("/{user_id}/", response_model=UserSchema)
async def get_user(
    user_id: int, user_repository: UserRepository = Depends(UserRepository.instance)
) -> UserModel:
    return user_repository.find_by_id(identifier=user_id)
