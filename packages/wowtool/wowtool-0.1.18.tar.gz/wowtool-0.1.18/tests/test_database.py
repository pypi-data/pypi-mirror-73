from cli.database import Database

# TODO: Load data into database

def test_live_streams_table_exist():
    database = Database()
    response = database.live_streams_table_exist()
    assert response in [False, True]

# def get_live_stream_id_from_name():
#     pass