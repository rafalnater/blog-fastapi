from abc import abstractmethod
from typing import List, Type

from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Date, Document, Text
from elasticsearch_dsl.connections import connections

from core.db import Base


class BaseDocument(Document):
    @staticmethod
    @abstractmethod
    def list_fields() -> List[str]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_model_identifier() -> str:
        raise NotImplementedError


class ElasticsearchDocumentHandler:
    document_class = None

    def __init__(self, document_class: Type[BaseDocument]):
        connections.create_connection(alias="default", hosts=['elasticsearch'])
        self.document_class = document_class

    def create_document(self, model: Base):
        self.document_class.init()  # TODO: move to app setup - migrations?

        document = self.document_class(
            meta={'id': self._get_document_index(model.id)}
        )

        for document_field_name in self.document_class.list_fields():
            setattr(document, document_field_name, getattr(model, document_field_name))

        document.save()

    def get_document(self, model_id: int) -> BaseDocument:
        document = self.document_class.get(
            id=self._get_document_index(model_id)
        )
        return document

    def update_document(self, model: Base):
        try:
            document = self.get_document(model.id)
        except NotFoundError:
            self.create_document(model)
            return

        for document_field_name in self.document_class.list_fields():
            setattr(document, document_field_name, getattr(model, document_field_name))

        document.save()

    def delete_document(self, model_id: int):
        try:
            document = self.get_document(model_id)
            document.delete()
        except NotFoundError:
            return

    def _get_document_index(self, model_id: int):
        return f"{self.document_class.get_model_identifier()}_{model_id}"
