import datetime
import uuid

from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel


class AuditoryModel(DjangoCassandraModel):
    __abstract__ = True

    created_by = columns.UUID(required=True, default=uuid.uuid4)
    created_date = columns.DateTime(required=True, default=datetime.datetime.now)
    updated_by = columns.UUID(required=True, default=uuid.uuid4)
    updated_date = columns.DateTime(required=True, default=datetime.datetime.now)
