import pytest
import time
from queupy import ExceptionQueueEmpty
from threading import Thread


def test_queue_push(queue):
    event = "test_event"
    payload = {"test": "payload"}
    queue.push(event, payload)
    assert queue.pop(event).payload == payload


def test_queue_pop(queue):
    event = "test_event"
    payload = {"test": "payload"}
    queue.push(event, payload)
    assert queue.pop(event).payload == payload
    try:
        queue.pop(event)
        assert False
    except ExceptionQueueEmpty:
        pass
    except Exception as e:
        assert False, e


def test_consume_push(queue):
    event = "test_event"
    payload = {"test": "payload"}
    queue.push(event, payload)
    assert next(queue.consume(event)).payload == payload


@pytest.mark.xfail()
@pytest.mark.timeout(2)
def test_lock_table(queue):
    event = "test_event"
    payload = {"test": "payload"}
    queue.push(event, payload)
    lock_string = "BEGIN WORK; LOCK TABLE {queue._meta.table_name};"
    queue._meta.database.execute_sql(lock_string)
    queue.pop(event)


def test_concurent_pop(queue):
    total_events = 100
    popped_events = []

    def produce():
        for i in range(total_events):
            queue.push("test_event", {"id": i})

    def consume():
        for event in queue.consume("test_event", frequency=0.01):
            popped_events.append(event.payload['id'])


    producers = [Thread(target=produce) for i in range(4)]
    consumer = Thread(target=consume)

    for producer in producers:
        producer.start()

    consumer.start()

    while True:
        if len(popped_events) >= total_events:
            break
        time.sleep(0.1)

    consumer.join()
    for producer in producers:
        producer.join()

    assert len(set(popped_events)) == total_events
