from cli.utils import get_base_file_path
from cli.constants import DATABASE_FILENAME
from tinydb import TinyDB, Query

class Database:

  def __init__(self, database_file_path=None):
    if not database_file_path:
      database_file_path = self.get_database_file_path()
    self.db = TinyDB(database_file_path)

  def get_database_file_path(self):
    file_path = get_base_file_path(DATABASE_FILENAME)
    return file_path

  def live_streams_table_exist(self):
    table_name = 'live_streams'
    tables = self.db.tables()
    exist = table_name in tables
    return exist

  def get_live_stream_id_from_name(self, name):
    id = None
    table_name = 'live_streams'
    query = Query()
    table = self.db.table(table_name)
    response = table.search(query.live_stream_name == name)
    if response:
      id = response[0].get('live_stream_id', None)
    return id

  def recordings_table_exist(self):
    table_name = 'recordings'
    tables = self.db.tables()
    exist = table_name in tables
    return exist

  def get_recording_id_from_name(self, name):
    id = None
    table_name = 'recordings'
    query = Query()
    table = self.db.table(table_name)
    response = table.search(query.live_stream_name == name)
    if response:
      id = response[0].get('recording_id', None)
    return id

  def insert_live_streams_document(self, document_batch):
    table_name = 'live_streams'
    self.db.drop_table(table_name)
    table = self.db.table(table_name)
    table.insert_multiple(document_batch)

  def insert_recordings_document(self, document_batch):
    table_name = 'recordings'
    self.db.drop_table(table_name)
    table = self.db.table(table_name)
    table.insert_multiple(document_batch)
