from typing import Type

import pytest

from core.db import Base
from core.mapper import AbstractMapper, ModelType, SchemaType
from core.repository import AbstractRepository
from core.security import password_hashing
from core.settings import settings


class TestSettings:
    def test_database_uri_is_not_none(self):
        assert settings.SQLALCHEMY_DATABASE_URI is not None

    def test_assemble_db_connection_when_v_is_string(self):
        assert settings.assemble_db_connection(v="test", values={}) == "test"

    def test_assemble_cors_origins(self):
        assert settings.assemble_cors_origins(v="test1,test2") == ["test1", "test2"]
        assert settings.assemble_cors_origins(v=["test"]) == ["test"]
        with pytest.raises(ValueError):
            settings.assemble_cors_origins(v=True)


class TestMapper:
    def test_not_implemented_methods(self):
        class ImproperlyImplementedMapper(AbstractMapper):
            @staticmethod
            def schema_to_model(schema: SchemaType) -> ModelType:
                return AbstractMapper.schema_to_model(schema)

        with pytest.raises(NotImplementedError):
            ImproperlyImplementedMapper.schema_to_model(None)


class TestRepository:
    def test_not_implemented_methods(self):
        class ImproperlyImplementedRepository(AbstractRepository):
            def _get_model_class(self) -> Type[Base]:
                return super()._get_model_class()

            def _get_mapper(self) -> Type[AbstractMapper]:
                return super()._get_mapper()

        repository = ImproperlyImplementedRepository(per_page=1, db=None)

        with pytest.raises(NotImplementedError):
            repository._get_model_class()

        with pytest.raises(NotImplementedError):
            repository._get_mapper()


class TestSecurity:
    def test_hashing(self):
        phrase = "Test123#"
        phrase_hash = password_hashing.generate_hash(phrase)

        assert password_hashing.verify_hash(phrase, phrase_hash)
