from core.db import Base
from elasticsearch_dsl import Date, Document, Text
from elasticsearch_dsl.connections import connections


DOCUMENT_ACTION_CREATE = 'create'
DOCUMENT_ACTION_UPDATE = 'update'


def save_elasticsearch_document(model: Base, document_class: Document, action: str):
    connections.create_connection(alias="default", hosts=['elasticsearch'])
    document_class.init()

    if action == DOCUMENT_ACTION_CREATE:
        document = document_class(
            meta={'id': model.id}
        )
    else:
        document = document_class.get(id=model.id)

    for (document_field_name, _, _) in document_class._ObjectBase__list_fields():
        setattr(document, document_field_name, getattr(model, document_field_name))

    document.save()
