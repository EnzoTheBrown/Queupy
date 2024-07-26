import pytest
from queupy import init_queue, ExceptionQueueEmpty


@pytest.fixture()
def queue():
    queue = init_queue(
        database_name='queupy',
        user='queupy',
        password='queupy',
        host='localhost',
    )
    yield queue
    queue.drop_table()

