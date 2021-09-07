from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

from core.db import Base


ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class AbstractMapper(ABC, Generic[SchemaType, ModelType]):
    @staticmethod
    @abstractmethod
    def schema_to_model(schema: SchemaType) -> ModelType:
        raise NotImplementedError
