import pytest
from cli.database import Database

@pytest.fixture
def database():
    database = Database(database_file_path='tests/fixtures/test_database.json')
    return database

def test_live_streams_table_exist(mocker, database):
    exist = database.live_streams_table_exist()
    assert exist in [False, True]

def test_get_live_stream_id_from_name(mocker, database):
    id = database.get_live_stream_id_from_name('Baton-6945748')
    assert id=='ww7jxjtw'