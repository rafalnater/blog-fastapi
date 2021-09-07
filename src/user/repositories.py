from typing import Type

from core.repository import AbstractRepository
from user.mappers import UserCreationMapper
from user.models import User as UserModel
from user.schemas import User as UserSchema


class UserRepository(AbstractRepository[UserModel, int, UserSchema]):
    def _get_model_class(self) -> Type[UserModel]:
        return UserModel

    def _get_mapper(self) -> Type[UserCreationMapper]:
        return UserCreationMapper
