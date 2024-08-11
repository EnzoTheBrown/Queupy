from queupy import init_queue, LIFOEventQueue, FIFOEventQueue
import pytest
from os import environ

HOST = environ.get('DB_HOST', 'localhost')
USER = environ.get('DB_USER', 'queupy')
PASSWORD = environ.get('DB_PASSWORD', 'queupy')
DATABASE_NAME = environ.get('DB_NAME', 'queupy')
PORT = environ.get('DB_PORT', 5432)


@pytest.fixture()
def event_queue():
    event_queue = init_queue(
        database_name=DATABASE_NAME,
        host=HOST,
        user=USER,
        password=PASSWORD,
        port=PORT,
    )
    yield event_queue

    cur = event_queue.conn.cursor()
    cur.execute(f"DROP TABLE {event_queue.table_name}")
    event_queue.conn.commit()
    cur.close()
    event_queue.conn.close()


@pytest.fixture()
def event_queue_lifo():
    event_queue = init_queue(
        database_name='queupy',
        host='localhost',
        user='queupy',
        password='queupy',
        policy=LIFOEventQueue
    )

    yield event_queue

    cur = event_queue.conn.cursor()
    cur.execute(f"DROP TABLE {event_queue.table_name}")
    event_queue.conn.commit()
    cur.close()
    event_queue.conn.close()

