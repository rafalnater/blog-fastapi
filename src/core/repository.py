from __future__ import annotations

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Generic, List, Type, TypeVar

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.db import Base, get_db
from core.mapper import AbstractMapper
from core.settings import settings


ModelType = TypeVar("ModelType", bound=Base)
IdentifierType = TypeVar("IdentifierType")
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class AbstractRepository(ABC, Generic[ModelType, IdentifierType, SchemaType]):
    @abstractmethod
    def _get_model_class(self) -> Type[Base]:
        raise NotImplementedError

    @abstractmethod
    def _get_mapper(self) -> Type[AbstractMapper]:
        raise NotImplementedError

    def __init__(self, per_page: int, db: Session):
        self._per_page = per_page
        self._db = db

    @classmethod
    async def instance(
        cls, db: Session = Depends(get_db)
    ) -> AsyncGenerator[AbstractRepository, None]:
        yield cls(per_page=settings.PER_PAGE_RESULTS, db=db)

    def all(self, offset: int = 0) -> List[ModelType]:
        model_class = self._get_model_class()
        return self._db.query(model_class).offset(offset).limit(self._per_page).all()

    def find_by_id(self, identifier: IdentifierType) -> ModelType:
        model_class = self._get_model_class()
        return self._db.query(model_class).get(identifier)

    def create(self, schema: SchemaType) -> ModelType:
        mapper = self._get_mapper()
        model = mapper.schema_to_model(schema)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return model
