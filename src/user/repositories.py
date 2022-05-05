from typing import Type

from core.repository import AbstractRepository
from core.security import password_hashing
from user.mappers import UserCreationMapper
from user.models import User as UserModel
from user.schemas import User as UserSchema


class UserRepository(AbstractRepository[UserModel, int, UserSchema]):
    def _get_model_class(self) -> Type[UserModel]:
        return UserModel

    def _get_mapper(self) -> Type[UserCreationMapper]:
        return UserCreationMapper

    def get_user(self, email: str):
        return self._db.query(self._get_model_class()).filter_by(email=email).first()

    def authenticate_user(self, email: str, password: str):
        user = self.get_user(email=email)
        if not user:
            return False
        if not password_hashing.verify_hash(password=password, hash=user.hashed_password):
            return False
        return user
