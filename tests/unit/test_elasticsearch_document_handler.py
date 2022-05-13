from datetime import datetime

from elasticsearch_dsl import Date, Document, Text
from unittest.mock import Mock
from unittest.mock import patch

from core.elasticsearch import BaseDocument, ElasticsearchDocumentHandler


class TestElasticsearchDocumentHandler:
    @patch('core.elasticsearch.connections')
    def test_create_document(self, connections_mock):
        document_class = self._get_test_document_class()
        document_class.init = Mock()
        document_class.save = Mock()

        elasticsearch_document_handler = ElasticsearchDocumentHandler(
            document_class=document_class
        )
        elasticsearch_document_handler.create_document(self._get_test_model())

        document_class.init.assert_called_once()
        document_class.save.assert_called_once()
        connections_mock.create_connection.assert_called_once_with(
            alias='default',
            hosts=['elasticsearch'],
        )

    @patch('core.elasticsearch.connections')
    def test_update_document(self, connections_mock):
        document_class = self._get_test_document_class()
        document_class.get = Mock()
        document_class.save = Mock()

        elasticsearch_document_handler = ElasticsearchDocumentHandler(
            document_class=document_class
        )
        elasticsearch_document_handler.update_document(self._get_test_model())

        document_class.get.assert_called_once()
        document_class.save.assert_called_once()
        connections_mock.create_connection.assert_called_once_with(
            alias='default',
            hosts=['elasticsearch'],
        )

    @patch('core.elasticsearch.connections')
    def test_delete_document(self, connections_mock):
        document_class = self._get_test_document_class()
        document_class.get = Mock()
        document_class.delete = Mock()

        elasticsearch_document_handler = ElasticsearchDocumentHandler(
            document_class=document_class
        )
        elasticsearch_document_handler.delete_document(self._get_test_model().id)

        document_class.get.assert_called_once()
        document_class.delete.assert_called_once()
        connections_mock.create_connection.assert_called_once_with(
            alias='default',
            hosts=['elasticsearch'],
        )

    def _get_test_document_class(self):
        class TestDocument(BaseDocument):
            title = Text()
            pub_date = Date()

            class Index:
                name = 'test'

            @staticmethod
            def list_fields():
                return 'title', 'pub_date'

            @staticmethod
            def get_model_identifier():
                return 'T'

        return TestDocument

    def _get_test_model(self):
        class TestModel:
            id = int
            title = str
            pub_date = datetime

        test_model = TestModel()
        test_model.id = 1
        test_model.title = 'test title'
        test_model.pub_date = '2022-05-12T07:34:58'

        return test_model
