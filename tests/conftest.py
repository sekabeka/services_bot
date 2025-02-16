import pytest
import peewee

from settings import DATABASE_FOR_TESTING
from core.models import Record, Service


@pytest.fixture(scope="class")
def test_db():
    database = peewee.PostgresqlDatabase(**DATABASE_FOR_TESTING)
    models = [Record, Service]
    database.bind(models)
    database.connect()
    database.create_tables(models)
    yield database
    database.drop_tables(models)
    database.close()
