from core.mapper import AbstractMapper
from core.security import password_hashing
from user.models import User as UserModel
from user.schemas import UserCreate as UserCreateSchema


class UserCreationMapper(AbstractMapper[UserCreateSchema, UserModel]):
    @staticmethod
    def schema_to_model(schema: UserCreateSchema) -> UserModel:
        return UserModel(
            email=schema.email,
            hashed_password=password_hashing.generate_hash(schema.password),
        )
