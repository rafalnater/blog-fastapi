from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from core.settings import settings
from user.auth_utils import create_access_token
from user.models import User as UserModel
from user.repositories import UserRepository
from user.schemas import User as UserSchema
from user.schemas import UserCreate as UserCreateSchema
from user.schemas import Token

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


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: UserRepository = Depends(UserRepository.instance),
):
    user = user_repository.authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
