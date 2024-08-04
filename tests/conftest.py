from queupy import init_queue, LIFOEventQueue, FIFOEventQueue
import pytest


@pytest.fixture()
def event_queue():
    event_queue = init_queue(
        database_name='queupy',
        host='localhost',
        user='queupy',
        password='queupy',
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

